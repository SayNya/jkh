from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Questions(models.Model):
    text = models.TextField()
    is_closed = models.BooleanField(default=False)


class Comments(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
