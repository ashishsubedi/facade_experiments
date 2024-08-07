from services.function_registry import register_function

@register_function
async def postprocess_products(data: dict):
    print("Post-processing procucts response")
    # Implement post-processing logic for users
    new_data = []
    for d in data:
        new_data.append({
            k:v for k, v in d.items() if k in ("id", "title", "price")
        })
    return new_data