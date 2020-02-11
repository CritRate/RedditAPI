from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Comment, Community, Post

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
