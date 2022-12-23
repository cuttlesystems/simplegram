from rest_framework.exceptions import APIException


class InvalidBotTokenWhenGenerateBot(APIException):
    status_code = 400
    default_detail = 'Given bot token must not be empty.'
    default_code = 'invalid_bot_token'


class ErrorsFromBotGenerator(APIException):
    status_code = 500
    default_detail = 'Some error when generating bot'
    default_code = 'error'
