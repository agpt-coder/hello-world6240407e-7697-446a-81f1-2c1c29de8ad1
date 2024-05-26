from pydantic import BaseModel


class HelloWorldRequestModel(BaseModel):
    """
    Request model for the /hello endpoint. As it is a public access endpoint and doesn't require any input parameters, this model will be empty.
    """

    pass


class HelloWorldResponseModel(BaseModel):
    """
    Response model for the /hello endpoint. This model will have a single field to return the 'hello world' string response.
    """

    message: str


def sayHelloWorld(request: HelloWorldRequestModel) -> HelloWorldResponseModel:
    """
    Returns a simple 'hello world' message. This endpoint is the core feature of the 'hello world' app and is publicly accessible. Expected response is a plain text message: 'hello world'.

    Args:
    request (HelloWorldRequestModel): Request model for the /hello endpoint. As it is a public access endpoint and doesn't require any input parameters, this model will be empty.

    Returns:
    HelloWorldResponseModel: Response model for the /hello endpoint. This model will have a single field to return the 'hello world' string response.

    Example:
        request = HelloWorldRequestModel()
        response = sayHelloWorld(request)
        print(response.message)  # 'hello world'
    """
    return HelloWorldResponseModel(message="hello world")
