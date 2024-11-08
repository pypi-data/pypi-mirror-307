class VMMethodError(Exception):
    def __init__(self, message) -> None:
        super().__init__(f"{message}")
