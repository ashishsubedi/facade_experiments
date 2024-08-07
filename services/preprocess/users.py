from fastapi import Request
from services.function_registry import register_function

# Define pre-processing and post-processing functions
@register_function
async def preprocess_users(request: Request):
    print("Pre-processing users request")
    # Implement pre-processing logic for users
