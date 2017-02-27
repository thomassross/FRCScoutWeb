from django.conf.urls import url

from . import views

app_name = "teams"
urlpatterns = [
    url(r"^new_team/", views.new_team, name="new_team"),
    url(r"^edit_team/(?P<team_number>[0-9]+)/", views.edit_team, name="edit_team"),
    url(r"^toggle_favorite/", views.toggle_favorite, name="toggle_favorite")
]
