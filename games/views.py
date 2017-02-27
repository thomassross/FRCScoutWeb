from django.shortcuts import render, redirect


def index(request):
    return render(request, "games/index.html")


def select_year(request, new_year):
    request.session["user_selected_year"] = new_year

    return redirect(request.GET.get("next", "/"))
