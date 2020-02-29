from django.db import models


class PostManager(models.Manager):

    def create_post(self, name: str, body: str):
        return self.create(name=name, body=body)


class CommentManager(models.Manager):

    def get_community_comments(self, community: str):
        return self.filter(comment__post__community=community)
