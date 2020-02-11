from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from .managers import PostManager, CommentManager

import uuid

User = get_user_model()


class Community(models.Model):
    name = models.CharField(blank=False, null=False, max_length=32, primary_key=True)
    moderators = models.ManyToManyField(User, related_name='community_moderators')

    def __str__(self):
        return self.name


class Post(models.Model):
    # /id/slug -> unique address for the same post slug
    id = models.CharField(max_length=6, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=128)
    body = models.TextField(default='', null=False)
    slug = models.SlugField(blank=False, null=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    objects = PostManager()

    def __str__(self):
        return f'[id:{self.id}]Post:{self.name} by {self.user} in {self.community} community: {self.body}'

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name))
        # generate random 6 letter key
        while True:
            new_id = str(uuid.uuid4()).lower()[:6]
            if not Post.objects.filter(id=new_id).exists():
                break
        self.id = new_id
        return super().save(*args, **kwargs)


class Comment(models.Model):
    id = models.CharField(max_length=6, unique=True, primary_key=True)
    text = models.TextField(blank=False, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # null: top comment, id: reply to a comment
    reply_id = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    objects = CommentManager()

    def save(self, *args, **kwargs):
        # generate random 6 letter key
        while True:
            new_id = str(uuid.uuid4()).lower()[:6]
            if not Comment.objects.filter(id=new_id).exists():
                break
        self.id = new_id
        return super().save(*args, **kwargs)
