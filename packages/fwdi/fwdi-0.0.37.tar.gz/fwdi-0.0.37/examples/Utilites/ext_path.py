import os


class ExtPath:

    def __init__(self) -> None:
        pass

    def exists_or_create_path(path: str) -> bool:
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            isExist = True
        return isExist

    def exists_file(path: str):
        isExist = os.path.exists(path)
        return isExist