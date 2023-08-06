class APIException(Exception):
    def __init__(self, status, content, *args: object) -> None:
        self.status = status
        self.content = content
        super().__init__(self.status, self.content, args)
    