from urllib.parse import urlparse, urlunparse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from FRCScoutWeb.utils import get_user_selected_year
from teams.models import Team
from .forms import NewTeamForm, EditTeamForm


@login_required
def new_team(request):
    user_selected_year = get_user_selected_year(request)

    if request.method == "POST":
        form = NewTeamForm(request.POST)
        form.prepare_tasks(user_selected_year)

        if form.is_valid():
            do_continue = True

            if not form.cleaned_data["team_number"] or form.cleaned_data["team_number"] < 0:
                form.add_error("team_number", "Invalid team number.")
                do_continue = False

            if do_continue:
                team_number = form.cleaned_data["team_number"]
                name = form.cleaned_data["team_name"] or "Team #{}".format(team_number)

                auto_points = form.cleaned_data["auto_points"] or 0
                tasks = form.cleaned_data["tasks"]

                favorite = form.cleaned_data["favorite"] or False

                team = Team(team_number=team_number)

                team.name = name
                team.auto_points = auto_points
                team.favorite = favorite

                team.save()

                for task in tasks:
                    team.tasks.add(task)

                if "next" in request.GET:
                    parsed_url = urlparse(request.GET["next"])
                    query = QueryDict(parsed_url.query, True)
                    query["add_team_success"] = True
                    query["add_team_team_number"] = form.cleaned_data.get("team_number")
                    next_url = urlunparse(
                        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, query.urlencode(),
                         parsed_url.fragment))
                else:
                    query = QueryDict(mutable=True)
                    query["add_team_success"] = True
                    query["add_team_team_number"] = form.cleaned_data.get("team_number")
                    next_url = reverse("teams:new_team") + "?" + query.urlencode()

                return redirect(next_url)
    else:
        form = NewTeamForm()
        form.prepare_tasks(user_selected_year)

    return render(request, "teams/new_team.html", {"form": form})


@login_required
def edit_team(request, team_number):
    user_selected_year = get_user_selected_year(request)
    team = get_object_or_404(Team, team_number=team_number)

    if request.method == "POST":
        form = EditTeamForm(request.POST)
        form.prepare_tasks(user_selected_year)

        if form.is_valid():
            name = form.cleaned_data["team_name"] or "Team #{}".format(team_number)

            auto_points = form.cleaned_data["auto_points"] or 0
            tasks = form.cleaned_data["tasks"]

            favorite = form.cleaned_data["favorite"] or False

            team.name = name
            team.auto_points = auto_points
            team.favorite = favorite

            team.save()

            team.tasks.clear()
            for task in tasks:
                team.tasks.add(task)

            if "next" in request.GET:
                parsed_url = urlparse(request.GET["next"])
                query = QueryDict(parsed_url.query, True)
                query["edit_team_success"] = True
                query["edit_team_team_number"] = team_number
                next_url = urlunparse(
                    (parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, query.urlencode(),
                     parsed_url.fragment))
            else:
                query = QueryDict(mutable=True)
                query["edit_team_success"] = True
                query["edit_team_team_number"] = team_number
                next_url = reverse("home:index") + "?" + query.urlencode()

            return redirect(next_url)
    else:
        # FIXME: This should probably be a ModelForm
        initial = {"team_name": team.name,
                   "auto_points": team.auto_points,
                   "tasks": team.tasks.all(),
                   "favorite": team.favorite}

        form = EditTeamForm(initial)

        form.prepare_tasks(user_selected_year)

    return render(request, "teams/edit_team.html", {"team_number": team_number, "form": form})


def toggle_favorite(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    if "team_number" not in request.POST or "year" not in request.POST:
        return HttpResponse(status=404)

    team_number = request.POST.get("team_number")
    year = request.POST.get("year")

    team = get_object_or_404(Team, team_number=team_number, year=year)
    team.favorite = not team.favorite
    team.save()

    return HttpResponse(content=str(team.favorite))
