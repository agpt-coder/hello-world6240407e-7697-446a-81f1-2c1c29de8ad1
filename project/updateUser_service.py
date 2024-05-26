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


class UpdateUserResponse(BaseModel):
    """
    The response model for updating a user. It returns the updated user details.
    """

    id: int
    email: str
    password: str
    role: Role


async def updateUser(
    id: int, email: Optional[str], password: Optional[str], role: Role
) -> UpdateUserResponse:
    """
    This endpoint updates the details of a specific user based on the provided user ID in the path parameter.
    It expects updated user details in the request body. Only authenticated users can access this endpoint.

    Args:
        id (int): The user ID of the specific user to be updated.
        email (Optional[str]): The new email for the user. This field should be unique.
        password (Optional[str]): The new password for the user.
        role (Role): The new role for the user. It should be one of the predefined roles (Admin/User).

    Returns:
        UpdateUserResponse: The response model for updating a user. It returns the updated user details.

    Example:
        updateUser(1, "new_email@example.com", "new_password", Role.Admin)
        > UpdateUserResponse(id=1, email="new_email@example.com", password="new_password", role=Role.Admin)
    """
    data_to_update = {}
    if email:
        existing_user = await prisma.models.User.prisma().find_first(
            where={"email": email}
        )
        if existing_user and existing_user.id != id:
            raise ValueError("Email already exists.")
        data_to_update["email"] = email
    if password:
        data_to_update["password"] = password
    if role is not None:
        data_to_update["role"] = role.value
    if not data_to_update:
        raise ValueError("No data provided to update the user.")
    updated_user = await prisma.models.User.prisma().update(
        where={"id": id}, data=data_to_update
    )
    if not updated_user:
        raise ValueError("Failed to update the user.")
    return UpdateUserResponse(
        id=updated_user.id,
        email=updated_user.email,
        password=updated_user.password,
        role=Role(updated_user.role),
    )
