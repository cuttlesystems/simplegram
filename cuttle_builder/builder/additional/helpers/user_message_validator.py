import re
from typing import List

from b_logic.data_objects import BotMessage, MessageTypeEnum


class UserMessageValidator:
    def __init__(self, messages: List[BotMessage]):
        self._user_variables = self._get_all_user_variables(messages)

    def _add_curly_brackets(self, text: str) -> str:
        return f'{{{text}}}'

    def _get_all_variables_from_text(self, text: str) -> List[str]:
        # todo replace using regex
        pattern = re.escape("{") + ".+?" + re.escape("}")
        variables: List[str] = re.findall(pattern, text)
        return variables

    def _add_curly_brackets_for_user_variables(self) -> List[str]:
        return [self._add_curly_brackets(variable) for variable in self._user_variables]

    def _replace_matched_substring_in_text(self, text: str, match: str) -> str:
        return text.replace(match, self._add_curly_brackets(match))

    def get_validated_message_text(self, text: str) -> str:
        variables: List[str] = self._get_all_variables_from_text(text)
        all_variables_in_curly_brackets = self._add_curly_brackets_for_user_variables()
        for match in variables:
            if match not in all_variables_in_curly_brackets:
                text = self._replace_matched_substring_in_text(text, match)
        return text

    def get_variables_from_text_exist_in_user_variables(self, text: str) -> List[str]:
        variables = []
        for variable in self._user_variables:
            if self._add_curly_brackets(variable) in text:
                variables.append(variable)
        return variables

    def _get_all_user_variables(self, messages: List[BotMessage]) -> List[str]:
        return [message.variable for message in messages if message.message_type==MessageTypeEnum.ANY_INPUT]
