from django.db import models
from django.contrib.auth import get_user_model
from model_utils.models import TimeStampedModel

User = get_user_model()


class Post(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_by_user")
    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'post'

    def __str__(self):
        return self.title


class Like(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_by_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_liked")

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"

    def __str__(self):
        return self.post.title
