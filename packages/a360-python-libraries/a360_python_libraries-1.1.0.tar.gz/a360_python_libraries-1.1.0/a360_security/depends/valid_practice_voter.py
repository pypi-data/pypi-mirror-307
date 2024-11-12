from fastapi import Depends, HTTPException, status

from ..dto import UserDTO
from .user_dependant import require_user
from a360_services import get_practice_service


def valid_practice():
    def practice_checker(
            user: UserDTO = Depends(require_user),
            a360_practice=Depends(get_practice_service),
    ):
        if user.is_practice_dependant:
            if user.practice_id is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User does not have a practice associated"
                )
            if not a360_practice.is_practice_active(user.practice_id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Practice is not active"
                )

    return practice_checker
