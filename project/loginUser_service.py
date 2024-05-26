from enum import Enum

import bcrypt
import jwt
from pydantic import BaseModel


class Role(Enum):
    """
    Enum representing user roles.
    """

    Admin: str
    User: str


class UserDetails(BaseModel):
    """
    Model representing the user's details.
    """

    id: int
    email: str
    role: Role


class LoginResponse(BaseModel):
    """
    Response model for a successful login. It includes the JWT token and user details.
    """

    token: str
    user: UserDetails


SECRET_KEY = "your_jwt_secret_key"

ALGORITHM = "HS256"


async def loginUser(username: str, password: str) -> LoginResponse:
    """
    Authenticates an existing user. This function accepts a username and password, and if valid, returns a JWT token for subsequent authenticated requests.
    The expected response is the JWT token and user details.

    Args:
    username (str): The username of the user attempting to log in.
    password (str): The password of the user attempting to log in.

    Returns:
    LoginResponse: Response model for a successful login. It includes the JWT token and user details.

    Example:
    loginUser('testuser', 'password123')
    > LoginResponse(token='abc123', user=UserDetails(id=1, email='testuser@example.com', role=Role.User))
    """
    import prisma.models

    user = await prisma.models.User.prisma().find_first(where={"email": username})
    if not user or not bcrypt.checkpw(
        password.encode("utf-8"), user.password.encode("utf-8")
    ):
        raise ValueError("Invalid username or password")
    user_details = UserDetails(id=user.id, email=user.email, role=Role[user.role])
    token = jwt.encode(
        {"user_id": user.id, "role": user.role}, SECRET_KEY, algorithm=ALGORITHM
    )
    return LoginResponse(token=token, user=user_details)
