from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class Role(Enum):
    """
    Enum representing user roles.
    """

    Admin: str
    User: str


class CreateUserResponse(BaseModel):
    """
    Response model for the created user information.
    """

    id: int
    email: str
    role: Role


async def createUser(email: str, password: str, role: Role) -> CreateUserResponse:
    """
    This endpoint allows for the creation of a new user. It expects user details in the request body and returns the created user's information. Basic validation of input data should be performed here.

    Args:
    email (str): The email address of the new user. It must be unique.
    password (str): The password for the new user.
    role (Role): The role assigned to the new user, either 'User' or 'Admin'.

    Returns:
    CreateUserResponse: Response model for the created user information.

    Example:
        createUser("test@example.com", "password123", Role.User)
        > CreateUserResponse(id=1, email="test@example.com", role=Role.User)
    """
    created_user = await prisma.models.User.prisma().create(
        data={"email": email, "password": password, "role": role.name}
    )
    return CreateUserResponse(
        id=created_user.id, email=created_user.email, role=Role[created_user.role]
    )
