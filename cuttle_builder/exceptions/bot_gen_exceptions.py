class BotGeneratorException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class TokenException(BotGeneratorException):
    def __init__(self, msg: str):
        super().__init__(msg)


class NoOneMessageException(BotGeneratorException):
    def __init__(self, msg: str):
        super().__init__(msg)


class NoStartMessageException(BotGeneratorException):
    def __init__(self, msg: str):
        super().__init__(msg)


class WrongBracketsSyntaxError(BotGeneratorException):
    def __init__(self, msg: str):
        super().__init__(msg)


class GoToMessageHasNotNextMessageException(BotGeneratorException):
    def __init__(self, msg: str):
        super().__init__(msg)
