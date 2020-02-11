from rest_framework.test import APIClient, APITestCase
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from api.models import Comment, Post, Community

User = get_user_model()


class CommunityModelsTest(APITestCase):

    def test_string_representation(self):
        community = Community(name='django')
        self.assertEqual(str(community), community.name)

    def test_name_is_primary_key(self):
        community = Community.objects.create(name='django')
        self.assertEqual(community.pk, community.name)

    def test_cannot_save_empty_community(self):
        community = Community()
        with self.assertRaises(ValidationError):
            community.save()
            community.full_clean()

    def test_can_save_moderators(self):
        community = Community(name='django')
        community.full_clean()
        community.save()
        user_one = User.objects.create(username='user_one')
        user_two = User.objects.create(username='user_two')
        community.moderators.set([user_one, user_two])
        community.save()
        self.assertIn(user_one, community.moderators.all())
        self.assertIn(user_two, community.moderators.all())

    def test_cant_create_community_with_the_same_name(self):
        Community.objects.create(name='django')
        with self.assertRaises(IntegrityError):
            Community.objects.create(name='django')

    def test_name_cant_be_longer_than_32_characters(self):
        long_name = 'g' * 33
        with self.assertRaises(DataError):
            Community.objects.create(name=long_name)

    # def test_cant_have_more_that_ten_moderators(self):
    #     community = Community.objects.create(name='django')
    #     users = []
    #     for i in range(15):
    #         users.append(User.objects.create(username='crit' + str(i)))
    #     with self.assertRaises(IntegrityError):
    #         community.moderators.set(users)
    #         community.save()
    #         print(community.moderators.all())


class PostModelsTest(APITestCase):

    def setUp(self) -> None:
        self.user_one = User.objects.create(username='user_one')
        self.com_django = Community.objects.create(name='django')
        self.data_one = {
            'user': self.user_one,
            'community': self.com_django,
            'name': 'Testing in django',
            'body': 'How to test using mocks?'
        }
        self.data_two = {
            'user': self.user_one,
            'community': self.com_django,
            'name': 'Testing in django',
            'body': 'How to test using mocks?'
        }

    def test_string_representation(self):
        post = Post.objects.create(**self.data_one)
        self.assertEqual(
            str(post),
            f'[id:{post.id}] Post:{post.name} by {post.user} in {post.community} community: {post.body}'
        )

    def test_id_is_6_characters_long(self):
        post_one = Post.objects.create(**self.data_one)
        self.assertEqual(len(post_one.id), 6)

    def test_post_have_unique_ids(self):
        post_one = Post.objects.create(**self.data_one)
        post_two = Post.objects.create(**self.data_two)
        self.assertNotEqual(post_one.id, post_two.id)

    def test_post_create_slug(self):
        post_one = Post.objects.create(**self.data_one)
        self.assertEqual(post_one.slug, 'testing-in-django')

    def test_change_to_post_body_doesnt_change_id(self):
        post_one = Post.objects.create(**self.data_one)
        old_id = post_one.id
        post_one.body = 'new body'
        post_one.save()
        new_id = post_one.id
        self.assertEqual(old_id, new_id)

    def test_to_post_body_make_edited_true(self):
        post_one = Post.objects.create(**self.data_one)
        self.assertFalse(post_one.edited)
        post_one.body = 'new body'
        post_one.save()
        self.assertTrue(post_one.edited)


class CommentModelsTest(APITestCase):

    def setUp(self) -> None:
        self.user_one = User.objects.create(username='user_one')
        com = Community.objects.create(name='django')
        self.post = Post.objects.create(
            user=self.user_one,
            community=com,
            name='Testing in django',
            body='How to test using mocks?'
        )
        self.data = {
            'text': 'just use documentation',
            'user': self.user_one,
            'post': self.post
        }

    def test_string_representation(self):
        comment = Comment.objects.create(**self.data)
        self.assertEqual(
            str(comment),
            f'[id:{comment.id}] Comment: {comment.text} by User: {comment.user} in Post: {comment.post.name}'
        )

    def test_default_value_for_reply_id_is_none(self):
        comment = Comment.objects.create(**self.data)
        self.assertIsNone(comment.reply_id)

    def test_comments_have_different_ids(self):
        comment_one = Comment.objects.create(**self.data)
        comment_two = Comment.objects.create(**self.data)
        self.assertNotEqual(comment_one.id, comment_two.id)

    def test_comment_id_does_not_change(self):
        comment = Comment.objects.create(**self.data)
        old_id = comment.id
        comment.text = 'new text'
        comment.save()
        new_id = comment.id
        self.assertEqual(old_id, new_id)

    def test_edited_comment_changes_flag_to_true(self):
        comment = Comment.objects.create(**self.data)
        self.assertFalse(comment.edited)
        comment.text = 'new text'
        comment.save()
        self.assertTrue(comment.edited)

    def test_reply_id_contains_correct_top_comment(self):
        top_comment = Comment.objects.create(**self.data)
        reply = Comment.objects.create(reply_id=top_comment, **self.data)
        self.assertEqual(reply.reply_id.id, top_comment.id)

    def test_id_is_6_letters_long(self):
        comment = Comment.objects.create(**self.data)
        self.assertEqual(len(comment.id), 6)
