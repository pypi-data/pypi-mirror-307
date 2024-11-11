import inspect


def handle_page_error(cls):
    for name, method in vars(cls).items():
        if (
            callable(method)
            and not inspect.isclass(method)
            and not name.startswith("__")
        ):
            setattr(
                cls,
                name,
                handle_page_errors(method),
            )

    return cls


def handle_page_errors(method):
    def wrapper(*args, **kwargs):
        try:
            result = method(*args, **kwargs)
            return result
        except Exception as e:
            message = f"Unable to do {method.__name__}"

            if str(e) != message:
                raise RuntimeError(message) from e

            raise e

    return wrapper
