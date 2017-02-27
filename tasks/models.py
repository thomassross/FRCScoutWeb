from django.db import models


class Task(models.Model):
    codeyear = models.CharField(primary_key=True, unique=True, max_length=50)
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.name
