import prisma
import prisma.models
from pydantic import BaseModel


class GetUserResponseModel(BaseModel):
    """
    The response model containing the details of the user identified by the provided user ID.
    """

    id: int
    email: str
    role: str


async def getUser(id: int) -> GetUserResponseModel:
    """
    This endpoint retrieves the details of a specific user based on the provided user ID in the path parameter. It is a protected endpoint that requires a valid token for access.

    Args:
    id (int): The unique identifier of the user to retrieve.

    Returns:
    GetUserResponseModel: The response model containing the details of the user identified by the provided user ID.

    Example:
        user = await getUser(1)
        > GetUserResponseModel(id=1, email='example@example.com', role='User')
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": id})
    if user is None:
        raise ValueError(f"User with ID {id} not found")
    return GetUserResponseModel(id=user.id, email=user.email, role=user.role)
