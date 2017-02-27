from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import ugettext_lazy as _


class FSWAuthForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={"autofocus": "", "required": "",
                                      "class": "mdc-textfield__input mdc-typography"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput({"class": "mdc-textfield__input mdc-typography",
                                    "required": ""}))
