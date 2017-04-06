from django.db import models
from tasks.models import Task

from FRCScoutWeb.config import CURRENT_FRC_YEAR


class Team(models.Model):
    team_number = models.IntegerField()
    name = models.CharField(max_length=100)

    tasks = models.ManyToManyField(Task, blank=True)
    auto_points = models.IntegerField(default=0)

    year = models.IntegerField(default=CURRENT_FRC_YEAR)

    favorite = models.BooleanField(default=False)

    notes = models.CharField(max_length=5000, blank=True, default="")

    rating = models.IntegerField(default=0)

    class Meta:
        unique_together = ("team_number", "year")

    def __str__(self):
        return "{}".format(self.team_number, self.name, self.year)
