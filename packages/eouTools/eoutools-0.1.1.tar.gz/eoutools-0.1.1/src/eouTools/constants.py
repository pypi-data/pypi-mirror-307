class Constant:
    def __init__(self, value):
        self.value = value

    def __get__(self, obj, type=None):
        return self.value

    def __set__(self, instance, value):
        raise PermissionError(f"{self.__name__} is a constant.")
