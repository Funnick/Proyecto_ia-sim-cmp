class ReturnException(Exception):
    def __init__(self, value, type, *args: object) -> None:
        super().__init__(*args)
        self.value = value
        self.type = type
