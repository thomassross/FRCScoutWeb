import json
import string

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.crypto import get_random_string

from api.models import APIKey
from tasks.models import Task
from teams.models import Team


@login_required
def generate_api_key(request):
    def get_unique_key():
        rtn_key = get_random_string(length=32, allowed_chars=string.ascii_letters + string.digits)

        if APIKey.objects.filter(key=rtn_key).exists():
            return get_unique_key()
        else:
            return rtn_key

    key = get_unique_key()

    if "app_name" not in request.GET:
        return HttpResponse("{\"status\": 1}", status=400)

    api_key = APIKey(key=key)
    api_key.user = request.user
    api_key.app_name = request.GET["app_name"]
    api_key.save()

    content = json.dumps({
        "status": 0,
        "key": key
    })

    return HttpResponse(content, status=200)


def get_team(request, year, team_number):
    key = request.GET.get("key", "")

    if not APIKey.objects.filter(key=key).exists():
        return HttpResponse("{\"status\": 1}", status=401)

    try:
        team = Team.objects.get(team_number=team_number, year=year)
    except Team.DoesNotExist:
        return HttpResponse("{\"status\": 1}", status=400)

    tasks_obj = {}
    team_tasks = team.tasks.all()
    for task in Task.objects.filter(year=year):
        tasks_obj[task.codeyear] = {
            "name": task.name,
            "team_able": task in team_tasks
        }

    content = json.dumps({
        "status": 0,
        "key": key,
        "team_number": team.team_number,
        "name": team.name,
        "tasks": tasks_obj,
        "auto_points": team.auto_points,
        "year": team.year,
        "favorite": team.favorite
    })

    return HttpResponse(content, status=200)
