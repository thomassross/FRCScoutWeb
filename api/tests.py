import json

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from api.models import APIKey
from tasks.models import Task
from teams.models import Team


class GenerateAPIKeyTests(TestCase):
    def setUp(self):
        user = User.objects.create(username="test_user")
        user.save()

        self.client = Client()
        self.client.force_login(user)

    def test_generate_api_key_success(self):
        response = self.client.get(reverse("api:generate_api_key") + "?app_name=Test")
        self.assertEqual(response.status_code, 200)

    def test_generate_api_key_no_appname(self):
        response = self.client.get(reverse("api:generate_api_key"))
        self.assertEqual(response.status_code, 400)


class GetTeamTest(TestCase):
    def setUp(self):
        task1 = Task(codeyear="task-1")
        task1.name = "Task"
        task1.year = 1
        task1.save()

        task2 = Task(codeyear="othertask-1")
        task2.name = "Other Task"
        task2.year = 1
        task2.save()

        team1 = Team(team_number=1, year=1)
        team1.name = "1"
        team1.auto_points = 100
        team1.favorite = False
        team1.save()
        team1.tasks.add(task1)

        user = User.objects.create(username="test_user")
        user.save()

        key = APIKey(key="test_key")
        key.app_name = "django_test"
        key.user = user
        key.save()

        self.client = Client()

    def test_get_team_success(self):
        response = self.client.get(reverse("api:get_team", args=[1, 1]) + "?key=test_key")

        self.assertEqual(response.status_code, 200)

        parsed_response = json.loads(str(response.content.decode("UTF-8")))

        self.assertEqual(parsed_response["status"], 0)
        self.assertEqual(parsed_response["name"], "1")
        self.assertEqual(parsed_response["auto_points"], 100)
        self.assertEqual(parsed_response["favorite"], False)
        self.assertTrue("tasks" in parsed_response)

        task1_expected = {
            "codeyear": "task-1",
            "name": "Task",
            "team_able": True
        }

        task2_expected = {
            "codeyear": "othertask-1",
            "name": "Other Task",
            "team_able": False
        }

        tasks_expected = [
            task1_expected,
            task2_expected
        ]

        self.assertEqual(parsed_response["tasks"], tasks_expected)

    def test_get_team_no_or_wrong_key(self):
        response = self.client.get(reverse("api:get_team", args=[1, 1]))
        self.assertEqual(response.status_code, 401)

        response = self.client.get(reverse("api:get_team", args=[1, 1]) + "?key=garbage_key")
        self.assertEqual(response.status_code, 401)
