class BotGeneratorException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class TokenException(BotGeneratorException):
    def __init__(self, msg: str):
        super().__init__(msg)
