from django.conf.urls import url

from . import views

app_name = "api"
urlpatterns = [
    url(r"^generate_api_key/$", views.generate_api_key, name="generate_api_key"),
    url(r"^get_team/(?P<year>[0-9]+)/(?P<team_number>[0-9]+)/$", views.get_team, name="get_team"),
    url(r"^set_team/(?P<year>[0-9]+)/(?P<team_number>[0-9]+)/$", views.set_team, name="set_team")
]