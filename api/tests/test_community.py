from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from api.models import Community

from django.urls import reverse
from django.contrib.auth import get_user_model
import json

User = get_user_model()


class TestCreateCommunity(APITestCase):

    def setUp(self) -> None:
        self.django_community = 'django'
        self.user = User.objects.create(username='crit')

    def test_can_create_community(self):
        data = {
            'name': self.django_community
        }
        response = self.client.post(reverse('get_post_community'), data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
