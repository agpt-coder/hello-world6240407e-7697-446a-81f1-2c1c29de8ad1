import prisma
import prisma.models
from pydantic import BaseModel


class HealthCheckRequestModel(BaseModel):
    """
    Request model for the HealthCheck endpoint. Since this is a simple GET request without any parameters, this model is empty.
    """

    pass


class HealthCheckResponseModel(BaseModel):
    """
    Response model for the HealthCheck endpoint. This will return a simple plain text response 'hello world' indicating the app is running properly.
    """

    message: str


async def get_health_status(
    request: HealthCheckRequestModel,
) -> HealthCheckResponseModel:
    """
    This endpoint serves as a health check for the app. When a GET request is made to this endpoint, it returns a plain text response 'hello world'.
    This indicates that the application is running properly. The route does not require any authentication and is accessible to anyone.

    Args:
        request (HealthCheckRequestModel): Request model for the HealthCheck endpoint. Since this is a simple GET request without any parameters,
                                           this model is empty.

    Returns:
        HealthCheckResponseModel: Response model for the HealthCheck endpoint. This will return a simple plain text response 'hello world'
                                  indicating the app is running properly.

    Example:
        request = HealthCheckRequestModel()
        response = await get_health_status(request)
        print(response)
        > HealthCheckResponseModel(message='hello world')
    """
    health_check_module = await prisma.models.HealthCheckModule.prisma().find_first()
    message = health_check_module.content if health_check_module else "hello world"
    return HealthCheckResponseModel(message=message)
