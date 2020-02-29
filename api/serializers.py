from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Comment, Community, Post
from accounts.serializers import  UserSerializer

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommunitySerializer(serializers.ModelSerializer):
    moderators = UserSerializer(many=True)

    class Meta:
        model = Community
        fields = ('name', 'moderators')
