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


async def checkHealth(request: HealthCheckRequestModel) -> HealthCheckResponseModel:
    """
    Checks the health of the API service. This endpoint simply returns a 'healthy' status if the service is running properly.
    It interacts with the HealthCheckModule. Expected response is a JSON object indicating the service health status.

    Args:
    request (HealthCheckRequestModel): Request model for the HealthCheck endpoint. Since this is a simple GET request without any parameters, this model is empty.

    Returns:
    HealthCheckResponseModel: Response model for the HealthCheck endpoint. This will return a simple plain text response 'hello world' indicating the app is running properly.

    Example:
        request = HealthCheckRequestModel()
        response = checkHealth(request)
        > HealthCheckResponseModel(message='hello world')
    """
    health_check_module = await prisma.models.HealthCheckModule.prisma().find_first()
    message = health_check_module.content if health_check_module else "hello world"
    return HealthCheckResponseModel(message=message)
