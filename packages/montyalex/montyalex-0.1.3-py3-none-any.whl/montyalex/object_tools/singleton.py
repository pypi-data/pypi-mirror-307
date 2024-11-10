def singleton_decorator(get_identifier=None):
    def wrapper(cls):
        instances = {}
        def get_instance(*args, **kwargs):
            if get_identifier:
                identifier = get_identifier(*args, **kwargs)
            else:
                identifier = None
            key = (cls, identifier)
            if key not in instances:
                instances[key] = cls(*args, **kwargs)
            return instances[key]
        return get_instance
    return wrapper
