from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User, UserSession
from .tests_base import user_data, updated_user_data, user_session_data


class UserAPITests(APITestCase):
    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/v1/users/'
        self.client = APIClient()
        self.user = User.objects.create_user(**user_data)
        self.user_token = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.user_token.access_token}'
        )

        self.session = UserSession.objects.create(
            user=self.user, **user_session_data
        )

    def test_get_user_profile_success(self):
        url = f'{self.base_url}profile/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], self.user.email)

    def test_update_user_profile_success(self):
        url = f'{self.base_url}profile/'
        response = self.client.patch(url, json=updated_user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['data']['firstName'], 'user'
        )

    def test_get_user_sessions_success(self):
        url = f'{self.base_url}sessions/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
        self.assertEqual(
            response.data['data'][0]['authSSID'], self.session.authSSID
        )

    def test_close_session_success(self):
        url = f'{self.base_url}close/session/{self.session.authSSID}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            UserSession.objects.filter(authSSID=self.session.authSSID).exists()
        )

    def test_close_sessions_success(self):
        url = f'{self.base_url}close/sessions/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserSession.objects.count(), 1)
