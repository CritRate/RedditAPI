from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.exceptions import ValidationError

from api.models import Community

from django.urls import reverse
from django.contrib.auth import get_user_model
import json

User = get_user_model()


class TestCreateCommunity(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.django_community = 'django'
        self.user = User.objects.create(username='crit')
        self.data = {
            'name': self.django_community,
            'moderators': [
                {'username': self.user.username}
            ]
        }
        self.client.force_authenticate(user=self.user)

    def test_create_community_with_valid_user(self):
        response = self.client.post(reverse('get_post_community'), data=json.dumps(self.data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(b'crit', response.content)

    def test_cant_create_existing_community(self):
        self.client.post(reverse('get_post_community'), data=json.dumps(self.data),
                         content_type='application/json')
        response = self.client.post(reverse('get_post_community'), data=json.dumps(self.data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'name', response.content)

    def test_cant_create_community_with_invalid_user(self):
        self.data['moderators'][0]['username'] = 'anon'
        response = self.client.post(reverse('get_post_community'), data=json.dumps(self.data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'moderators', response.content)

    def test_create_community_with_two_mods(self):
        User.objects.create(username='anon')
        self.data['moderators'].append({'username': 'anon'})
        response = self.client.post(reverse('get_post_community'), data=json.dumps(self.data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(b'anon', response.content)
        self.assertIn(b'crit', response.content)

    def test_cant_create_community_with_one_wrong_mod(self):
        self.data['moderators'].append({'username': 'user'})
        response = self.client.post(reverse('get_post_community'), data=json.dumps(self.data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'User with username: user does not exist.', response.content)

    def test_cant_create_community_with_duplicate_users(self):
        self.data['moderators'].append({'username': 'crit'})
        response = self.client.post(reverse('get_post_community'), data=json.dumps(self.data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
