import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponseModel(BaseModel):
    """
    Response model for deleting a user. It confirms whether the deletion was successful or not.
    """

    message: str


async def deleteUser(id: int) -> DeleteUserResponseModel:
    """
    Deletes a specific user by user ID. This endpoint requires an authenticated request with a valid JWT token and user authorization.
    Expected response is a success message on successful deletion.

    Args:
        id (int): The ID of the user to be deleted.

    Returns:
        DeleteUserResponseModel: Response model for deleting a user. It confirms whether the deletion was successful or not.

    Example:
        deleteUser(1)
        > DeleteUserResponseModel(message="User successfully deleted.")
    """
    user = await prisma.models.User.prisma().delete(where={"id": id})
    if user:
        return DeleteUserResponseModel(message="User successfully deleted.")
    else:
        return DeleteUserResponseModel(message="User not found.")
