from django.db import models

from django.conf import settings


class APIKey(models.Model):
    key = models.TextField(max_length=50, unique=True, primary_key=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    app_name = models.TextField(max_length=255)
