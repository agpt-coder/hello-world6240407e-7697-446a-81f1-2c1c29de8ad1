import prisma
import prisma.models
from pydantic import BaseModel


class GetHelloRequest(BaseModel):
    """
    The request model for the 'GET /hello' endpoint. No input parameters needed.
    """

    pass


class GetHelloResponse(BaseModel):
    """
    The response model for the 'GET /hello' endpoint, returning the 'hello world' message.
    """

    message: str


async def getHelloWorld(request: GetHelloRequest) -> GetHelloResponse:
    """
    This endpoint returns a simple 'hello world' message. When invoked, the server will respond with a plain text message 'hello world'. This route serves as the primary and only functional endpoint of the application.

    Args:
        request (GetHelloRequest): The request model for the 'GET /hello' endpoint. No input parameters needed.

    Returns:
        GetHelloResponse: The response model for the 'GET /hello' endpoint, returning the 'hello world' message.

    Example:
        request = GetHelloRequest()
        response = await getHelloWorld(request)
        assert response.message == "hello world"
    """
    health_check_module = await prisma.models.HealthCheckModule.prisma().find_first()
    message = health_check_module.content if health_check_module else "hello world"
    response = GetHelloResponse(message=message)
    return response
