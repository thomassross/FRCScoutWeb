from django import forms
from django.core import validators

from FRCScoutWeb.config import CURRENT_FRC_YEAR, ALLOWED_YEARS
from FRCScoutWeb.widgets import MultipleCheckboxes, MaterialCheckboxInput

from tasks.models import Task


class NewTeamForm(forms.Form):
    team_number = forms.IntegerField(label="Team Number",
                                     widget=forms.NumberInput(attrs={"autofocus": "",
                                                                     "class": "mdc-textfield__input mdc-typography"}))

    team_name = forms.CharField(label="Team Name",
                                required=False,
                                widget=forms.TextInput(attrs={"class": "mdc-textfield__input mdc-typography"}))

    auto_points = forms.IntegerField(label="Autonomous Points",
                                     required=False,
                                     widget=forms.NumberInput(attrs={"autofocus": "",
                                                                     "class": "mdc-textfield__input mdc-typography"}))

    tasks = forms.ModelMultipleChoiceField(queryset=Task.objects.all(),
                                           # TODO: Maybe this can be replaced with forms.CheckboxSelectMultiple
                                           widget=MultipleCheckboxes,
                                           required=False)

    notes = forms.CharField(label="Notes",
                            required=False,
                            widget=forms.Textarea(attrs={"class": "mdc-textfield__input mdc-typography",
                                                         "cols": 25}))

    rating = forms.IntegerField(label="Rating",
                                required=False,
                                widget=forms.NumberInput(attrs={"class": "mdc-textfield__input mdc-typography",
                                                                "max": 10,
                                                                "min": 0}),
                                validators=[
                                    validators.MaxValueValidator(10),
                                    validators.MinValueValidator(0)
                                ],
                                help_text="Rating from 0 (worst) to 10 (best)")

    favorite = forms.BooleanField(label="Favorite", widget=MaterialCheckboxInput, required=False)

    def prepare_tasks(self, year=None):
        if not year or year not in ALLOWED_YEARS:
            year = CURRENT_FRC_YEAR

        self.fields["tasks"].queryset = Task.objects.filter(year=year)


class EditTeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name",
                                required=False,
                                widget=forms.TextInput(attrs={"class": "mdc-textfield__input mdc-typography"}))

    auto_points = forms.IntegerField(label="Autonomous Points",
                                     required=False,
                                     widget=forms.NumberInput(attrs={"autofocus": "",
                                                                     "class": "mdc-textfield__input mdc-typography"}))

    tasks = forms.ModelMultipleChoiceField(queryset=Task.objects.all(),
                                           # TODO: Maybe this can be replaced with forms.CheckboxSelectMultiple
                                           widget=MultipleCheckboxes,
                                           required=False)

    notes = forms.CharField(label="Notes",
                            required=False,
                            widget=forms.Textarea(attrs={"class": "mdc-textfield__input mdc-typography",
                                                         "cols": 25}))

    rating = forms.IntegerField(label="Rating",
                                required=False,
                                widget=forms.NumberInput(attrs={"class": "mdc-textfield__input mdc-typography",
                                                                "max": 10,
                                                                "min": 0}),
                                validators=[
                                    validators.MaxValueValidator(10),
                                    validators.MinValueValidator(0)
                                ],
                                help_text="Rating from 0 (worst) to 10 (best)")

    favorite = forms.BooleanField(label="Favorite", widget=MaterialCheckboxInput, required=False)

    def prepare_tasks(self, year=None):
        if not year or year not in ALLOWED_YEARS:
            year = CURRENT_FRC_YEAR

        self.fields["tasks"].queryset = Task.objects.filter(year=year)
