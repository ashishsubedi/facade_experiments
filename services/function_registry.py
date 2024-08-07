function_registry = {}

def register_function(func):
    function_registry[func.__name__] = func
    return func

