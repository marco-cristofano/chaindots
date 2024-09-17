from rest_framework import status
from rest_framework.test import APITestCase


class APICreateUserTest(APITestCase):
    url = '/api/users/'

    def test_create(self):
        params = {
            'username': 'username',
            'email': 'username@email.com',
            'password': 'password'
        }
        response = self.client.post(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 3)
        user = response.data
        self.assertIsNotNone(user['id'])
        self.assertEqual(user['username'], 'username')
        self.assertEqual(user['email'], 'username@email.com')


class APICreateUserFailTest(APITestCase):
    url = '/api/users/'

    def test_username_exists(self):
        params = {
            'username': 'username',
            'email': 'username@email.com',
            'password': 'password'
        }
        response = self.client.post(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(
            response, 'username already exists', status_code=400
        )
