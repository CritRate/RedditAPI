from rest_framework import serializers
from django.db import models
from django.contrib.auth import get_user_model

from .models import Comment, Community, Post
from accounts.serializers import UserCommunitySerializer

# from typing import List, OrderedDict

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


# class CommunityReadSerializer(serializers.ModelSerializer):
#     moderators = UserSerializer(many=True)
#
#     class Meta:
#         model = Community
#         fields = ('name', 'moderators')
#
#     def validate_moderators(self, data):
#         print('validate')
#         return data


class CommunityWriteSerializer(serializers.ModelSerializer):
    moderators = UserCommunitySerializer(many=True)

    class Meta:
        model = Community
        fields = ('name', 'moderators')

    def create(self, validated_data):
        moderators_data = validated_data.pop('moderators')
        community = Community.objects.create(**validated_data)
        for moderator_data in moderators_data:
            user = User.objects.get(username=moderator_data['username'])
            community.moderators.add(user)
        community.save()
        return community

    def validate_moderators(self, data):
        # test for maximum number of moderators
        if len(data) > 10:
            raise serializers.ValidationError('There can only be 10 mods in community.')
        # convert data to set to check for the same users in the list
        users = set()
        for user in data:
            users.add(('username', user['username']))
        if len(data) > len(users):
            raise serializers.ValidationError(f'All users should be distinct.')
        # check if user exist
        for user in data:
            username = user['username']
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError(f'User with username: {username} does not exist.')
        return data
