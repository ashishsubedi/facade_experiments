from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
import httpx
import json
from typing import Callable, Dict, Any
from services import function_registry

app = FastAPI()

# Load route configurations from a JSON file
with open("routes.json") as f:
    route_configs = json.load(f)

async def facade_handler(
    request: Request,
    config: Dict[str, Any],
    pre_process: Callable = None,
    post_process: Callable = None
):
    # Pre-processing
    if pre_process:
        await pre_process(request)
    
    # Make request to backend API
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=config["backend_url"],
            # headers=request.headers,
            params=request.query_params,
        )

    response_data = response.json()
    
    # Post-processing
    if post_process:
        response_data = await post_process(response_data)
    
    return JSONResponse(content=response_data, status_code=response.status_code)


# Dynamic route generation based on config
for route, config in route_configs.items():
    method = config.get("method", "GET")
    print(function_registry)
    pre_process = function_registry.get(config.get("pre_process"))
    post_process = function_registry.get(config.get("post_process"))

    def create_route_handler(config, pre_process, post_process):
        async def route_handler(request: Request):
            return await facade_handler(request, config, pre_process, post_process)
        return route_handler

    app.add_api_route(
        route, 
        create_route_handler(config, pre_process, post_process),
        methods=[method]
    )

# Define a simple endpoint
@app.get("/")
async def root():
    return {"message": "Facade API is running"}