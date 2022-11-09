import typing
import unittest
import uuid

import requests
import json

from tests.connection_settings import ConnectionSettings


class TestUserUrls(unittest.TestCase):
    def __init__(self, method_name: str):
        super().__init__(method_name)
        self._settings = ConnectionSettings()

    def test_user_creation_and_deletion(self):
        """
        Тестирование создания пользователя, получения, удаления
        """
        unique_username_suffix = '{0}'.format(str(uuid.uuid4()).replace('-', ''))

        test_name = "autotest_user_{0}".format(unique_username_suffix)

        # создаем пользователя
        create_user_response = requests.post(self._settings.site_addr + 'api/users/', {
            "first_name": "Autotest user {0}".format(unique_username_suffix),
            "last_name": "autotest_user {0}".format(unique_username_suffix),
            "username": test_name,
            "password": "1",
            "email": "autotest_user_{0}@cuttlesystems.com".format(unique_username_suffix)
        })
        self.assertEqual(create_user_response.status_code, 201)
        created_user_id = json.loads(create_user_response.text)['id']

        login_response = requests.post(
            self._settings.site_addr + 'api/auth/token/login/',
            {
                'username': test_name,
                'password': '1'
            }
        )
        self.assertEqual(login_response.status_code, 200)
        token = json.loads(login_response.text)['auth_token']

        # получаем созданного пользователя
        get_user_by_id_response = requests.get(
            self._settings.site_addr + 'api/users/{id}'.format(
                id=created_user_id),
            headers=self._get_headers(token)
        )
        self.assertEqual(get_user_by_id_response.status_code, 200)

        # для DELETE что-то автоматом content-type json не ставился
        headers_with_content_type = self._get_headers(token)
        headers_with_content_type['content-type'] = 'application/json'

        # удаляем созданного пользователя
        user_deletion_response = requests.delete(
            self._settings.site_addr + 'api/users/{id}/'.format(id=created_user_id),
            data=json.dumps({
                'current_password': '1'
            }),
            headers=headers_with_content_type
        )

        self.assertEqual(user_deletion_response.status_code, 204)
        print(user_deletion_response.text)
        print('user id {0}'.format(created_user_id))

    def _get_headers(self, token: str) -> dict:
        return {
            'Authorization': f'Token {token}'
        }
