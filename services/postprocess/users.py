from services.function_registry import register_function

@register_function
async def postprocess_users(data: dict):
    print("Post-processing users response")
    # Implement post-processing logic for users
    return data