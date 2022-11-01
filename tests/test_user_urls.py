import typing
import unittest
import uuid

import requests
import json

TESTING_SUITE = 'http://127.0.0.1:8000/'


class TestUserUrls(unittest.TestCase):
    def test_user_list(self):
        """
        Тестирование получения списка пользователей
        """
        get_users_response = requests.get(TESTING_SUITE + 'api/users')
        self.assertEqual(get_users_response.status_code, 200)
        users_data: typing.List[dict] = json.loads(get_users_response.text)
        usernames: typing.List[str] = [user['username'] for user in users_data]
        print(usernames)

    def test_user_creation_and_deletion(self):
        """
        Тестирование создания пользователя, получения, удаления
        """
        unique_username_suffix = '{0}'.format(str(uuid.uuid4()).replace('-', ''))

        # создаем пользователя
        create_user_response = requests.post(TESTING_SUITE + 'api/users/', {
            "first_name": "Autotest user {0}".format(unique_username_suffix),
            "last_name": "autotest_user {0}".format(unique_username_suffix),
            "username": "autotest_user_{0}".format(unique_username_suffix),
            "email": "autotest_user_{0}@cuttlesystems.com".format(unique_username_suffix)
        })
        self.assertEqual(create_user_response.status_code, 201)
        created_user_id = json.loads(create_user_response.text)['id']

        # получаем созданного пользователя
        get_user_by_id_response = requests.get(TESTING_SUITE + 'api/users/{id}'.format(
            id=created_user_id))
        self.assertEqual(get_user_by_id_response.status_code, 200)

        # удаляем созданного пользователя
        user_deletion_response = requests.delete(TESTING_SUITE + 'api/users/{id}'.format(
            id=created_user_id))
        self.assertEqual(user_deletion_response.status_code, 204)
        print(user_deletion_response.text)
        print('user id {0}'.format(created_user_id))

