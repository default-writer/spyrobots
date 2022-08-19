from functools import wraps

def update_env_func(name, value: dict):
    def wrapper(callback):
        @wraps(callback)
        def decorated(*args, **kwargs):
            kwargs.get(name, {}).update(value)
            return callback(*args, **kwargs)
        return decorated
    return wrapper
