from fastapi import Depends, HTTPException, status

from a360_security.enums.role import Role
from ..role_hierarchy import has_role
from ..utils.aws_cognito import AWSCognitoService, get_aws_cognito
from ..utils.bearer import get_token


async def get_current_user_roles(
        token: str = Depends(get_token),
        cognito_service: AWSCognitoService = Depends(get_aws_cognito)
) -> list[str]:
    user_data = cognito_service.get_current_user(token)
    return user_data.get("roles", [])


def require_role(*required_roles: Role):
    def role_checker(user_roles: list[str] = Depends(get_current_user_roles)):
        if not any(has_role(user_roles, role) for role in required_roles):
            roles_str = ", ".join([role.value for role in required_roles])
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions: requires one of {roles_str}"
            )
    return role_checker
