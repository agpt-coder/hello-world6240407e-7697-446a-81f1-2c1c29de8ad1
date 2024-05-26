import prisma
import prisma.models
from pydantic import BaseModel


class ApiDocsRequestModel(BaseModel):
    """
    Since this is a GET endpoint for documentation, no input parameters are needed.
    """

    pass


class ApiDocsResponseModel(BaseModel):
    """
    Response model detailing the documentation of the health check endpoint. It includes the path, method, expected response, and a brief explanation.
    """

    endpoint_path: str
    http_method: str
    description: str
    expected_response: str
    example_usage: str


async def getDocumentation(request: ApiDocsRequestModel) -> ApiDocsResponseModel:
    """
    This endpoint provides documentation for the available API endpoints. Specifically, it explains the health check/hello world endpoint, detailing the path, method, expected response, and usage. This documentation aids users in understanding how to interact with the API.

    Args:
        request (ApiDocsRequestModel): Since this is a GET endpoint for documentation, no input parameters are needed.

    Returns:
        ApiDocsResponseModel: Response model detailing the documentation of the health check endpoint. It includes the path, method, expected response, and a brief explanation.

    Example:
        request = ApiDocsRequestModel()
        getDocumentation(request)
        > ApiDocsResponseModel(endpoint_path="/health-check", http_method="GET", description="Health check endpoint", expected_response="hello world", example_usage="curl -X GET http://<host>/health-check")
    """
    doc_details = await prisma.models.APIDocumentationModule.prisma().find_first(
        where={"endpoint": "/health-check"}
    )
    if not doc_details:
        return ApiDocsResponseModel(
            endpoint_path="/health-check",
            http_method="GET",
            description="Health check endpoint",
            expected_response="hello world",
            example_usage="curl -X GET http://<host>/health-check",
        )
    return ApiDocsResponseModel(
        endpoint_path=doc_details.endpoint,
        http_method="GET",
        description="Health check endpoint",
        expected_response=doc_details.response,
        example_usage=f"curl -X GET http://<host>{doc_details.endpoint}",
    )
