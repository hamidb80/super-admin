from provider import services

def print(*args, **kwargs):
    return services.core.print(*args, **kwargs)

def input(*args, **kwargs):
    return services.core.input(*args, **kwargs)
