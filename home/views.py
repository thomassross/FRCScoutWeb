from django.shortcuts import render

from FRCScoutWeb.utils import get_user_selected_year
from tasks.models import Task
from teams.models import Team


def index(request):
    user_selected_year = get_user_selected_year(request)

    teams = Team.objects.filter(year=user_selected_year)
    teams = teams.order_by("-favorite", "team_number")

    num_tasks = len(Task.objects.filter(year=user_selected_year))

    return render(request, "home/index.html", {"teams": teams, "num_tasks": num_tasks})
