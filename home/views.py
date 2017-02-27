from django.shortcuts import render

from teams.models import Team
from tasks.models import Task

from FRCScoutWeb.config import CURRENT_FRC_YEAR, ALLOWED_YEARS


def index(request):
    user_selected_year = request.session.get("user_selected_year")
    if not user_selected_year or int(user_selected_year) not in ALLOWED_YEARS:
        request.session["user_selected_year"] = CURRENT_FRC_YEAR
        user_selected_year = CURRENT_FRC_YEAR

    teams = Team.objects.filter(year=user_selected_year)

    num_tasks = len(Task.objects.filter(year=user_selected_year))

    return render(request, "home/index.html", {"teams": teams, "num_tasks": num_tasks})
