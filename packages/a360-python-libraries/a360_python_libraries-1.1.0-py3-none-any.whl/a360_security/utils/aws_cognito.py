import base64
import hashlib
import hmac
import string
import random
import uuid

import boto3
import requests
import time

from jose import jwk, jwt
from jose.utils import base64url_decode
from fastapi import HTTPException, status

from ..enums import Role
from ..settings import settings


def generate_secure_password(length: int = 12) -> str:
    if length < 12:
        raise ValueError("Password length should be at least 12 characters.")

    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()-_"

    password = [
        random.choice(uppercase_letters),
        random.choice(lowercase_letters),
        random.choice(digits),
        random.choice(symbols)
    ]

    all_characters = uppercase_letters + lowercase_letters + digits + symbols
    password += random.choices(all_characters, k=length - 4)

    random.shuffle(password)

    return ''.join(password)


class AWSCognitoService:
    def __init__(self):
        self.region = settings.AWS_COGNITO_REGION
        self.user_pool_id = settings.AWS_COGNITO_USER_POOL_ID
        self.app_client_id = settings.AWS_COGNITO_APP_CLIENT_ID
        self.app_client_secret = settings.AWS_COGNITO_APP_CLIENT_SECRET
        self.keys_url = f'https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json'
        self.jwks = self._get_jwks()
        self.client = boto3.client('cognito-idp', region_name=self.region)

    def _get_jwks(self):
        response = requests.get(self.keys_url)
        response.raise_for_status()
        return response.json()['keys']

    def verify_token(self, token: str):
        header = jwt.get_unverified_header(token)
        kid = header['kid']

        key_index = -1
        for i in range(len(self.jwks)):
            if kid == self.jwks[i]['kid']:
                key_index = i
                break
        if key_index == -1:
            raise ValueError('Public key not found in jwks.json')

        public_key = jwk.construct(self.jwks[key_index])

        message, encoded_signature = str(token).rsplit('.', 1)
        decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise ValueError('Signature verification failed')

        claims = jwt.get_unverified_claims(token)

        if time.time() > claims['exp']:
            raise ValueError('Token is expired')

        return claims

    def get_user_data(self, token: str) -> dict:
        claims = self.verify_token(token)
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=claims.get("username")
            )
            is_active = response['Enabled']

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error retrieving user active status: {str(e)}"
            )

        return {
            "username": claims.get("username"),
            "email": claims.get("email", None),
            "sub": claims.get("sub"),
            "roles": claims.get("cognito:groups", []),
            "is_active": is_active
        }

    def get_current_user(self, token: str):
        try:
            return self.get_user_data(token)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_user_attributes(self, token: str) -> dict:
        try:
            response = self.client.get_user(AccessToken=token)
            user_attributes = {attr['Name']: attr['Value']
                               for attr in response['UserAttributes']}
            return user_attributes
        except self.client.exceptions.NotAuthorizedException as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Unauthorized: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error retrieving user attributes: {str(e)}"
            )

    def get_username_by_sub(self, user_sub: str) -> str:
        try:
            response = self.client.list_users(
                UserPoolId=self.user_pool_id,
                Filter=f'sub = "{user_sub}"'
            )

            if not response['Users']:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with sub {user_sub} not found"
                )

            return response['Users'][0]['Username']

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error retrieving username: {str(e)}"
            )

    def get_user_attributes_by_sub(self, user_sub: uuid.UUID) -> dict:
        try:
            response = self.client.list_users(
                UserPoolId=self.user_pool_id,
                Filter=f'sub = "{str(user_sub)}"'
            )

            if not response['Users']:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with sub {str(user_sub)} not found"
                )

            user = response['Users'][0]
            user_attributes = {attr['Name']: attr['Value']
                               for attr in user['Attributes']}
            return user_attributes

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error retrieving user attributes: {str(e)}"
            )

    def assign_role(self, user_sub: uuid.UUID, role: Role) -> None:
        try:
            username = self.get_username_by_sub(str(user_sub))

            self.client.admin_add_user_to_group(
                UserPoolId=self.user_pool_id,
                Username=username,
                GroupName=role.value
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to assign group: {str(e)}"
            )

    def unassign_role(self, user_sub: uuid.UUID, role: Role) -> None:
        try:
            username = self.get_username_by_sub(str(user_sub))

            self.client.admin_remove_user_from_group(
                UserPoolId=self.user_pool_id,
                Username=username,
                GroupName=role.value
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to unassign group: {str(e)}"
            )

    def get_secret_hash(self, email: str):
        message = email + self.app_client_id
        dig = hmac.new(
            self.app_client_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256).digest()
        return base64.b64encode(dig).decode()

    def activate_user(self, user_sub: uuid.UUID) -> None:
        try:
            username = self.get_username_by_sub(str(user_sub))

            self.client.admin_enable_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to activate user: {str(e)}"
            )

    def deactivate_user(self, user_sub: uuid.UUID) -> None:
        try:
            username = self.get_username_by_sub(str(user_sub))

            self.client.admin_disable_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to deactivate user: {str(e)}"
            )


def get_aws_cognito() -> AWSCognitoService:
    yield AWSCognitoService()
