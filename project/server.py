import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.checkHealth_service
import project.createUser_service
import project.deleteUser_service
import project.get_health_status_service
import project.getAPIDocumentation_service
import project.getDocumentation_service
import project.getHelloWorld_service
import project.getUser_service
import project.getUserDetails_service
import project.health_check_service
import project.loginUser_service
import project.registerUser_service
import project.sayHelloWorld_service
import project.updateUser_service
import project.updateUserDetails_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="hello world",
    lifespan=lifespan,
    description='create an app that has only one endpoint, that just returns "hello world"',
)


@app.get(
    "/health-check",
    response_model=project.health_check_service.HealthCheckResponseModel,
)
async def api_get_health_check(
    request: project.health_check_service.HealthCheckRequestModel,
) -> project.health_check_service.HealthCheckResponseModel | Response:
    """
    This endpoint serves as a health check for the application. When accessed with a GET request, it will return a simple text response of 'hello world'. This is used to indicate that the application is up and running. Since this is a basic status check, it should be publicly accessible to allow for easy monitoring by anyone or any automated system.
    """
    try:
        res = project.health_check_service.health_check(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/hello", response_model=project.getHelloWorld_service.GetHelloResponse)
async def api_get_getHelloWorld(
    request: project.getHelloWorld_service.GetHelloRequest,
) -> project.getHelloWorld_service.GetHelloResponse | Response:
    """
    This endpoint returns a simple 'hello world' message. When invoked, the server will respond with a plain text message 'hello world'. This route serves as the primary and only functional endpoint of the application.
    """
    try:
        res = await project.getHelloWorld_service.getHelloWorld(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/healthcheck",
    response_model=project.get_health_status_service.HealthCheckResponseModel,
)
async def api_get_get_health_status(
    request: project.get_health_status_service.HealthCheckRequestModel,
) -> project.get_health_status_service.HealthCheckResponseModel | Response:
    """
    This endpoint serves as a health check for the app. When a GET request is made to this endpoint, it returns a plain text response 'hello world'. This indicates that the application is running properly. The route does not require any authentication and is accessible to anyone.
    """
    try:
        res = await project.get_health_status_service.get_health_status(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/users/{userId}",
    response_model=project.deleteUser_service.DeleteUserResponseModel,
)
async def api_delete_deleteUser(
    id: int,
) -> project.deleteUser_service.DeleteUserResponseModel | Response:
    """
    Deletes a specific user by user ID. This endpoint requires an authenticated request with a valid JWT token and user authorization. Expected response is a success message on successful deletion.
    """
    try:
        res = await project.deleteUser_service.deleteUser(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/api/users/{userId}", response_model=project.updateUserDetails_service.UserResponse
)
async def api_put_updateUserDetails(
    id: int,
    email: Optional[str],
    password: Optional[str],
    role: project.updateUserDetails_service.Role,
) -> project.updateUserDetails_service.UserResponse | Response:
    """
    Updates details of a specific user by user ID. This endpoint accepts user attributes that need to be updated and requires an authenticated request with a valid JWT token. Expected response is the updated user details.
    """
    try:
        res = await project.updateUserDetails_service.updateUserDetails(
            id, email, password, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/api/users/login", response_model=project.loginUser_service.LoginResponse)
async def api_post_loginUser(
    username: str, password: str
) -> project.loginUser_service.LoginResponse | Response:
    """
    Authenticates an existing user. This endpoint accepts username and password, and if valid, returns a JWT token for subsequent authenticated requests. Expected response is the JWT token and user details.
    """
    try:
        res = await project.loginUser_service.loginUser(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/users/{userId}", response_model=project.getUserDetails_service.GetUserResponse
)
async def api_get_getUserDetails(
    userId: int,
) -> project.getUserDetails_service.GetUserResponse | Response:
    """
    Fetches details of a specific user by user ID. The endpoint requires an authenticated request with a valid JWT token. Expected response is the user’s profile data.
    """
    try:
        res = await project.getUserDetails_service.getUserDetails(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put("/users/:id", response_model=project.updateUser_service.UpdateUserResponse)
async def api_put_updateUser(
    id: int,
    email: Optional[str],
    password: Optional[str],
    role: project.updateUser_service.Role,
) -> project.updateUser_service.UpdateUserResponse | Response:
    """
    This endpoint updates the details of a specific user based on the provided user ID in the path parameter. It expects updated user details in the request body. Only authenticated users can access this endpoint.
    """
    try:
        res = await project.updateUser_service.updateUser(id, email, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/health-check",
    response_model=project.checkHealth_service.HealthCheckResponseModel,
)
async def api_get_checkHealth(
    request: project.checkHealth_service.HealthCheckRequestModel,
) -> project.checkHealth_service.HealthCheckResponseModel | Response:
    """
    Checks the health of the API service. This endpoint simply returns a 'healthy' status if the service is running properly. It interacts with the HealthCheckModule. Expected response is a JSON object indicating the service health status.
    """
    try:
        res = await project.checkHealth_service.checkHealth(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users/:id", response_model=project.getUser_service.GetUserResponseModel)
async def api_get_getUser(
    id: int,
) -> project.getUser_service.GetUserResponseModel | Response:
    """
    This endpoint retrieves the details of a specific user based on the provided user ID in the path parameter. It is a protected endpoint that requires a valid token for access.
    """
    try:
        res = await project.getUser_service.getUser(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/docs", response_model=project.getDocumentation_service.ApiDocsResponseModel
)
async def api_get_getDocumentation(
    request: project.getDocumentation_service.ApiDocsRequestModel,
) -> project.getDocumentation_service.ApiDocsResponseModel | Response:
    """
    This endpoint provides documentation for the available API endpoints. Specifically, it explains the health check/hello world endpoint, detailing the path, method, expected response, and usage. This documentation aids users in understanding how to interact with the API.
    """
    try:
        res = await project.getDocumentation_service.getDocumentation(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/hello-world",
    response_model=project.sayHelloWorld_service.HelloWorldResponseModel,
)
async def api_get_sayHelloWorld(
    request: project.sayHelloWorld_service.HelloWorldRequestModel,
) -> project.sayHelloWorld_service.HelloWorldResponseModel | Response:
    """
    Returns a simple 'hello world' message. This endpoint is the core feature of the 'hello world' app and is publicly accessible. Expected response is a plain text message: 'hello world'.
    """
    try:
        res = project.sayHelloWorld_service.sayHelloWorld(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.createUser_service.CreateUserResponse)
async def api_post_createUser(
    email: str, password: str, role: project.createUser_service.Role
) -> project.createUser_service.CreateUserResponse | Response:
    """
    This endpoint allows for the creation of a new user. It expects user details in the request body and returns the created user's information. Basic validation of input data should be performed here.
    """
    try:
        res = await project.createUser_service.createUser(email, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/users/register",
    response_model=project.registerUser_service.RegisterUserResponse,
)
async def api_post_registerUser(
    username: str, password: str, email: str
) -> project.registerUser_service.RegisterUserResponse | Response:
    """
    Registers a new user. This endpoint accepts user details like username, password, email, etc., and creates a new user record in the database. Expected response is a success message with the user's ID.
    """
    try:
        res = await project.registerUser_service.registerUser(username, password, email)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/documentation",
    response_model=project.getAPIDocumentation_service.GetAPIDocumentationResponse,
)
async def api_get_getAPIDocumentation(
    request: project.getAPIDocumentation_service.GetAPIDocumentationRequest,
) -> project.getAPIDocumentation_service.GetAPIDocumentationResponse | Response:
    """
    Provides API documentation to the users. This route is used to fetch detailed API documentation, explaining how each endpoint works, their request and response formats, and expected behaviors. It interacts with the APIDocumentationModule. Expected response is a JSON object containing API documentation.
    """
    try:
        res = await project.getAPIDocumentation_service.getAPIDocumentation(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
