from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from api.serializers import CommunityWriteSerializer
from api.models import Community

User = get_user_model()


class TestCommunitySerializer(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='crit')
        #  valid data
        self.serializer_data = {
            'name': 'django',
            'moderators': [
                {
                    'username': self.user.username
                }
            ]
        }

        self.serializer = CommunityWriteSerializer(data=self.serializer_data)

    def test_valid_community_serializer(self):
        self.assertTrue(self.serializer.is_valid())

    def test_invalid_user(self):
        self.serializer_data['moderators'].append({'username': 'anon'})
        self.assertFalse(self.serializer.is_valid())
        self.assertIn('moderators', self.serializer.errors)
        # Custom error message
        self.assertIn('User with username: anon does not exist.', self.serializer.errors['moderators'])

    def test_invalid_name(self):
        Community.objects.create(name='django')
        self.assertFalse(self.serializer.is_valid())
        self.assertIn('name', self.serializer.errors)

    def test_sets_community_moderator_when_created(self):
        self.serializer.is_valid()
        self.serializer.save()
        moderators = Community.objects.get(name=self.serializer_data['name']).moderators.all()
        self.assertIn(self.user, moderators)

    def test_maximum_moderator_count(self):
        for _ in range(10):
            self.serializer_data['moderators'].append({'username': 'crit'})
        self.assertFalse(self.serializer.is_valid())
        self.assertIn('There can only be 10 mods in community.',self.serializer.errors['moderators'])

    def test_moderators_are_distinct(self):
        for _ in range(5):
            self.serializer_data['moderators'].append({'username': 'crit'})
        self.assertFalse(self.serializer.is_valid())
        self.assertIn('All users should be distinct.', self.serializer.errors['moderators'])
