from enum import Enum
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Role(Enum):
    """
    Enum representing user roles.
    """

    Admin: str
    User: str


class UserResponse(BaseModel):
    """
    Response model for the updated user details.
    """

    id: int
    email: str
    role: Role


async def updateUserDetails(
    id: int, email: Optional[str], password: Optional[str], role: Role
) -> UserResponse:
    """
    Updates details of a specific user by user ID. This endpoint accepts user attributes that need to be updated and requires an authenticated request with a valid JWT token. Expected response is the updated user details.

    Args:
    id (int): The user ID of the specific user to be updated.
    email (Optional[str]): The new email for the user. This field should be unique.
    password (Optional[str]): The new password for the user.
    role (Role): The new role for the user. It should be one of the predefined roles (Admin/User).

    Returns:
    UserResponse: Response model for the updated user details.

    Example:
        await updateUserDetails(1, "newemail@example.com", "newpassword", Role.User)
        > UserResponse(
            id=1,
            email="newemail@example.com",
            role=Role.User
        )
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": id})
    if not user:
        raise ValueError(f"User with ID {id} does not exist")
    user_data = {}
    if email:
        user_data["email"] = email
    if password:
        user_data["password"] = password
    user_data["role"] = role.name
    updated_user = await prisma.models.User.prisma().update(
        where={"id": id}, data=user_data
    )
    return UserResponse(
        id=updated_user.id, email=updated_user.email, role=Role(updated_user.role)
    )
