import uuid

from fastapi import Depends

from ..enums import Role
from ..utils.aws_cognito import AWSCognitoService, get_aws_cognito
from ..dto import UserDTO
from ..utils.bearer import get_token
from ..role_hierarchy import ROLES_PRACTICE


def require_user(
        token: str = Depends(get_token),
        cognito_service: AWSCognitoService = Depends(get_aws_cognito)
) -> UserDTO:
    user_data = cognito_service.get_current_user(token)

    user_attributes = cognito_service.get_user_attributes(token)
    practice_id_str = user_attributes.get("custom:practice_id")
    practice_id = uuid.UUID(practice_id_str) if practice_id_str else None
    user_data["practice_id"] = practice_id
    user_data["is_admin"] = Role.ADMIN in user_data["roles"]
    user_data["is_practice_dependant"] = any(
        role in ROLES_PRACTICE for role in user_data["roles"]
    )

    return UserDTO(**user_data)
