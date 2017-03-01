import json
import string

import re
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from api.models import APIKey
from api.utils import is_valid_api_key
from tasks.models import Task
from teams.models import Team


@login_required
@csrf_exempt
def generate_api_key(request):
    def get_unique_key():
        new_key = get_random_string(length=32, allowed_chars=string.ascii_letters + string.digits)

        if is_valid_api_key(new_key):
            return get_unique_key()
        else:
            return new_key

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


@csrf_exempt
def get_team(request, year, team_number):
    key = request.GET.get("key", "")

    if not is_valid_api_key(key):
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


@csrf_exempt
def set_team(request, year, team_number):
    try:
        json_body = json.loads(request.body.decode("UTF-8"))
    except json.JSONDecodeError:
        return HttpResponse("{\"status\": 1}", status=400)

    key = json_body.get("key", "")

    if not is_valid_api_key(key):
        return HttpResponse("{\"status\": 1}", status=401)

    try:
        team = Team.objects.get(team_number=team_number, year=year)
    except Team.DoesNotExist:
        team = Team(team_number=team_number, year=year)

    if "name" in json_body:
        new_name = json_body["name"]
        if isinstance(new_name, str):
            team.name = new_name

    if "tasks" in json_body:
        team.tasks.clear()
        new_tasks = json_body["tasks"]
        if isinstance(new_tasks, dict):
            for codeyear, task in new_tasks.items():
                team_able = str(task["team_able"]).lower()
                if isinstance(task, dict) \
                        and isinstance(team_able, str) \
                        and isinstance(codeyear, str) \
                        and team_able == "true" \
                        and re.search("^\w+-\d+$", codeyear):
                    try:
                        task_obj = Task.objects.get(codeyear=codeyear)
                        team.tasks.add(task_obj)
                    except Task.DoesNotExist:
                        pass

    if "auto_points" in json_body:
        new_auto_points = json_body["auto_points"]
        if isinstance(new_auto_points, int):
            team.auto_points = int(new_auto_points)

    if "favorite" in json_body:
        new_favorite = json_body["favorite"]
        if isinstance(new_favorite, str):
            team.favorite = True if new_favorite.lower() == "true" else False

    team.save()

    return HttpResponse("{\"status\": 0}", status=200)
