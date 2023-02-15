import re
from typing import List

from b_logic.data_objects import BotMessage, MessageTypeEnum
from cuttle_builder.exceptions.bot_gen_exceptions import WrongBracketsSyntaxError


class UserMessageValidator:
    def __init__(self, messages: List[BotMessage]):
        self._user_variables = self._get_all_user_variables(messages)

    def get_validated_message_text(self, text: str) -> str:
        """
        double curly brackets of word in text, if it doesn't exist in user_variables
        Args:
            text: message from user

        Returns:
            (str) text, contains double curly brackets of words, that doesn't exist in user_variables
        """
        # найти и вернуть потенциальные переменные в тексте сообщенияs
        variables: List[str] = self._get_all_values_in_brackets(text)

        # добавить фигурные скобки ко всем, объявленным переменным
        all_variables_in_curly_brackets = self._add_curly_brackets_for_user_variables()

        # если переменная из текста сообщения не найдена среди всех заявленных переменных
        # то добавить к ней фигурные скобки
        for match in variables:
            if match not in all_variables_in_curly_brackets:
                text = self._replace_matched_substring_in_text(text, match)
        return text

    def get_variables_from_text_exist_in_user_variables(self, text: str) -> List[str]:
        """
        Find all variables in user text, that exist in user_variables and return them as array
        Args:
            text: message from user

        Returns:
            (List[str]) array of variables, matched in users message and in user_variables
        """
        variables = []
        for variable in self._user_variables:
            if self._add_curly_brackets(variable) in text:
                variables.append(variable)
        return variables

    def _add_curly_brackets_for_user_variables(self) -> List[str]:
        """
        Get each element of user_variables and add curly brackets to them
        Returns:
            (List[str]) array, contains user_variables in curly brackets
        """
        return [self._add_curly_brackets(variable) for variable in self._user_variables]

    def _add_curly_brackets(self, text: str) -> str:
        return f'{{{text}}}'

    def _get_all_variables_from_text(self, text: str) -> List[str]:
        """
        Find all words in curly brackets
        Args:
            text: message from user

        Returns:
            (List[str]) array of all words in curly brackets in text
        """
        # todo replace using regex
        pattern = re.escape("{") + ".+?" + re.escape("}")
        variables: List[str] = re.findall(pattern, text)
        return variables

    def _get_all_user_variables(self, messages: List[BotMessage]) -> List[str]:
        """
        Get list of all variables, that exist in bot
        Args:
            messages: bot messages

        Returns:
            (List[str]) list of all variables
        """
        return [message.variable for message in messages if message.message_type==MessageTypeEnum.ANY_INPUT]

    def _replace_matched_substring_in_text(self, text: str, match: str) -> str:
        """
        Replace substring in text with text and substring in curly brackets
        Args:
            text: text
            match: substring

        Returns:
            (str) text, contains substring in {curly brackets}
        """
        return text.replace(match, self._add_curly_brackets(match))

    def _get_all_values_in_brackets(self, string: str) -> List[str]:
        """
        Возвращает потенциальные переменные из текста сообщения, либо
        вызывает ошибку если присутствуют лишние фигурные скобки.

        Args:
            string: текст сообщения.

        Returns:
            список потенциальных переменных в фигурных скобках.
        """
        stack = []
        result = []
        start = 0
        for i, char in enumerate(string):
            if char == '{':
                if len(stack) == 0:
                    start = i + 1
                    stack.append(char)
                else:
                    raise WrongBracketsSyntaxError(
                        f"Error: Opening bracket after opening bracket in message - {string}")
            elif char == '}':
                if not stack:
                    raise WrongBracketsSyntaxError(
                        f"Error: Closing bracket without opening bracket in message - {string}")
                stack.pop()
                if not stack:
                    result.append('{' + string[start:i] + '}')
        if stack:
            raise WrongBracketsSyntaxError(
                f"Error: Opening bracket without closing bracket in message - {string}")
        return result
