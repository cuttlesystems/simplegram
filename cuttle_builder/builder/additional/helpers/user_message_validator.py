import re
from typing import List

from b_logic.data_objects import BotMessage, MessageTypeEnum


class UserMessageValidator():
    def __init__(self, messages: List[BotMessage]):
        self._user_variables = self._get_all_user_variables(messages)

    def _add_curly_brackets(self, text: str):
        return f'{{{text}}}'

    def get_validated_message_text(self, text: str):
        pattern = re.escape("{") + ".+?" + re.escape("}")
        variables: List[str] = re.findall(pattern, text)
        for match in variables:
            if match not in [self._add_curly_brackets(variable) for variable in self._user_variables]:
                text = text.replace(match, self._add_curly_brackets(match))
        return text

    def message_validation(self, text: str):
        variables = []
        for variable in self._user_variables:
            if self._add_curly_brackets(variable) in text:
                variables.append(variable)
        return variables

    def _get_all_user_variables(self, messages: List[BotMessage]):
        return [message.variable for message in messages if message.message_type==MessageTypeEnum.ANY_INPUT]
