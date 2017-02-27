from django import forms

from FRCScoutWeb.config import CURRENT_FRC_YEAR
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

    favorite = forms.BooleanField(label="Favorite", widget=MaterialCheckboxInput, required=False)

    def prepare_tasks(self, year=None):
        year = year or CURRENT_FRC_YEAR
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

    favorite = forms.BooleanField(label="Favorite", widget=MaterialCheckboxInput, required=False)

    def prepare_tasks(self, year=None):
        year = year or CURRENT_FRC_YEAR
        self.fields["tasks"].queryset = Task.objects.filter(year=year)
