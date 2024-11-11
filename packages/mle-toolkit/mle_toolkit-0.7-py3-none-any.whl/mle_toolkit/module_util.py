import importlib


def get_module(name: str):
    """
    Dynamic importing python modules
    Args:
        name: "sklearn.svm.SVC"
    Returns:
        sklearn.svm.SVC
    """
    module, function = name.rsplit(".", 1)
    module = importlib.import_module(module)
    return getattr(module, function)
