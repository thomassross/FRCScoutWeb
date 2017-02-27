from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout

from FRCScoutWeb.forms import FSWAuthForm

urlpatterns = [
    url(r"", include("home.urls")),
    url(r"^login/", login, {"authentication_form": FSWAuthForm}, name="login"),
    url(r'^logout/', logout, name="logout"),
    # TODO: other auth views
    url(r"^teams/", include("teams.urls")),
    url(r"^tasks/", include("tasks.urls")),
    url(r"^games/", include("games.urls")),
    url(r"^api/", include("api.urls")),
    url(r"^admin/", admin.site.urls)
]