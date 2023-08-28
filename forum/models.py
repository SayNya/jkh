from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Question(models.Model):
    title = models.CharField(max_length=80, default='')
    text = models.TextField()
    is_closed = models.BooleanField(default=False)
    comments = models.ManyToManyField(User, through='Comment')

    def __str__(self):
        return self.title


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user}, {self.created_at}'
