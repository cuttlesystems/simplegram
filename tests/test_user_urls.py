import typing
import unittest
import uuid

import requests
import json

TESTING_SUITE = 'http://127.0.0.1:8000/'


def get_headers(token: str) -> dict:
    return {
        'Authorization': f'Token {token}'
    }


class TestUserUrls(unittest.TestCase):
    # def test_user_list(self):
    #     """
    #     Тестирование получения списка пользователей
    #     """
    #     get_users_response = requests.get(TESTING_SUITE + 'api/users')
    #     self.assertEqual(get_users_response.status_code, 200)
    #     users_data: typing.List[dict] = json.loads(get_users_response.text)
    #     usernames: typing.List[str] = [user['username'] for user in users_data]
    #     print(usernames)

    def test_user_creation_and_deletion(self):
        """
        Тестирование создания пользователя, получения, удаления
        """
        unique_username_suffix = '{0}'.format(str(uuid.uuid4()).replace('-', ''))

        test_name = "autotest_user_{0}".format(unique_username_suffix)

        # создаем пользователя
        create_user_response = requests.post(TESTING_SUITE + 'api/users/', {
            "first_name": "Autotest user {0}".format(unique_username_suffix),
            "last_name": "autotest_user {0}".format(unique_username_suffix),
            "username": test_name,
            "password": "1",
            "email": "autotest_user_{0}@cuttlesystems.com".format(unique_username_suffix)
        })
        self.assertEqual(create_user_response.status_code, 201)
        created_user_id = json.loads(create_user_response.text)['id']

        login_response = requests.post(
            TESTING_SUITE + 'api/auth/token/login/',
            {
                'username': test_name,
                'password': '1'
            }
        )
        self.assertEqual(login_response.status_code, 200)
        token = json.loads(login_response.text)['auth_token']

        # получаем созданного пользователя
        get_user_by_id_response = requests.get(
            TESTING_SUITE + 'api/users/{id}'.format(
                id=created_user_id),
            headers=get_headers(token)
        )
        self.assertEqual(get_user_by_id_response.status_code, 200)

        # удаляем созданного пользователя
        # user_deletion_response = requests.Request(
        #     TESTING_SUITE + 'api/users/{id}'.format(id=created_user_id),
        #     data={
        #         'current_password': '1'
        #     },
        #     headers=get_headers(token)
        # )

        he = get_headers(token)
        he["content-type"] = "application/json"

        session = requests.Session()
        delete_user_request = requests.Request(
            method='DELETE',
            url=TESTING_SUITE + 'api/users/{id}/'.format(id=created_user_id),
            data=json.dumps({
                'current_password': '1'
            }),

            headers=he
        )
        prepared = session.prepare_request(delete_user_request)
        user_deletion_response = session.send(prepared)

        self.assertEqual(user_deletion_response.status_code, 204)
        print(user_deletion_response.text)
        print('user id {0}'.format(created_user_id))
