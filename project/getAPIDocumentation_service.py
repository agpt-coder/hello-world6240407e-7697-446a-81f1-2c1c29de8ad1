import prisma
import prisma.models
from pydantic import BaseModel


class GetAPIDocumentationRequest(BaseModel):
    """
    Request model for fetching API documentation. Since this is a GET endpoint, no additional parameters are required.
    """

    pass


class GetAPIDocumentationResponse(BaseModel):
    """
    Response model for API documentation. This includes details about every endpoint, their request formats, response formats, and behaviors.
    """

    id: int
    title: str
    endpoint: str
    response: str


async def getAPIDocumentation(
    request: GetAPIDocumentationRequest,
) -> GetAPIDocumentationResponse:
    """
    Provides API documentation to the users. This route is used to fetch detailed API documentation, explaining how each endpoint works, their request and response formats, and expected behaviors. It interacts with the APIDocumentationModule. Expected response is a JSON object containing API documentation.

    Args:
    request (GetAPIDocumentationRequest): Request model for fetching API documentation. Since this is a GET endpoint, no additional parameters are required.

    Returns:
    GetAPIDocumentationResponse: Response model for API documentation. This includes details about every endpoint, their request formats, response formats, and behaviors.

    Example:
    request = GetAPIDocumentationRequest()
    res = await getAPIDocumentation(request)
    print(res)
    > GetAPIDocumentationResponse(id=1, title="API Documentation", endpoint="/health-check", response="hello world")
    """
    documentation = await prisma.models.APIDocumentationModule.prisma().find_first()
    if documentation:
        return GetAPIDocumentationResponse(
            id=documentation.id,
            title=documentation.title,
            endpoint=documentation.endpoint,
            response=documentation.response,
        )
    else:
        raise ValueError("API Documentation not found")
