from django.conf.urls import url

from . import views

app_name = "games"
urlpatterns = [
    url(r"^$", views.index, name="index"),
    # FIXME: home:index hardcodes this URL pattern
    url(r"^select/(?P<new_year>[0-9]+)/$", views.select_year, name="select_year")
]
