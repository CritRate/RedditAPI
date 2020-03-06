from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.exceptions import ValidationError

from api.models import Community

from django.urls import reverse
from django.contrib.auth import get_user_model
import json

User = get_user_model()


class TestUserView(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(username='crit', password='164964')
        self.data = {
            'username': 'crit',
            'password': 164964
        }

    def test_get_token(self):
        response = self.client.post(reverse('get_auth_token'), data=json.dumps(self.data),
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn(b'token', response.content)
