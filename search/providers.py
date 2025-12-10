provider_registry = []

def register_global_search_provider(func):
    provider_registry.append(func)
    return func
