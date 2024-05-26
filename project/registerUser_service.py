import prisma
import prisma.models
from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    """
    Response model for the user registration endpoint. It includes a success message and the ID of the newly created user.
    """

    message: str
    user_id: int


async def registerUser(
    username: str, password: str, email: str
) -> RegisterUserResponse:
    """
    Registers a new user. This endpoint accepts user details like username, password, email, etc., and creates a new user record in the database. Expected response is a success message with the user's ID.

    Args:
    username (str): The username for the new user.
    password (str): The password for the new user.
    email (str): The email address for the new user.

    Returns:
    RegisterUserResponse: Response model for the user registration endpoint. It includes a success message and the ID of the newly created user.

    Example:
        await registerUser("john_doe", "securepassword123", "john.doe@example.com")
        > RegisterUserResponse(message="User successfully registered", user_id=1)
    """
    user = await prisma.models.User.prisma().create(
        data={"email": email, "password": password}
    )
    return RegisterUserResponse(message="User successfully registered", user_id=user.id)
