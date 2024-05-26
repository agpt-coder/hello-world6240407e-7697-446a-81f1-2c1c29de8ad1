import prisma
import prisma.models
from pydantic import BaseModel


class GetUserResponse(BaseModel):
    """
    The user profile data corresponding to the given user ID.
    """

    id: int
    email: str
    role: str


async def getUserDetails(userId: int) -> GetUserResponse:
    """
    Fetches details of a specific user by user ID. The endpoint requires an authenticated request with a valid JWT token. Expected response is the user’s profile data.

    Args:
      userId (int): The ID of the user to fetch.

    Returns:
      GetUserResponse: The user profile data corresponding to the given user ID.

    Example:
      userDetails = await getUserDetails(1)
      # GetUserResponse(id=1, email='john.doe@example.com', role='Admin')
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not user:
        raise ValueError(f"User with ID {userId} not found")
    return GetUserResponse(id=user.id, email=user.email, role=user.role)
