import copy

from django.forms import Widget, CheckboxInput
from django.forms.utils import flatatt
from django.utils.datastructures import MultiValueDict

from django.utils.encoding import force_text

from django.utils.html import format_html
from django.utils.safestring import mark_safe


class MultipleCheckboxes(Widget):
    dont_use_model_field_default_for_empty_data = True

    def __init__(self, attrs=None, choices=()):
        super(MultipleCheckboxes, self).__init__(attrs)

        self.choices = list(choices)

    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.attrs = self.attrs.copy()
        obj.choices = copy.copy(self.choices)
        memo[id(self)] = obj
        return obj

    def render(self, name, value, attrs=None):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html("<div {}>", flatatt(final_attrs))]
        checkboxes = self.render_checkboxes(value, name)
        if checkboxes:
            output.append(checkboxes)
        output.append("</div>")
        return mark_safe("\n".join(output))

    @staticmethod
    def render_checkbox(selected_choices, checkbox_value, checkbox_label, name):
        if checkbox_value is None:
            checkbox_value = ""

        checkbox_value = force_text(checkbox_value)
        if checkbox_value in selected_choices:
            selected_html = mark_safe("checked=\"checked\"")
        else:
            selected_html = ""

        output = [
            "<div class=\"mdc-form-field\">"
            "<div class=\"mdc-checkbox\" data-mdc-auto-init=\"MDCCheckbox\">",
            format_html("<input type=\"checkbox\" id=\"checkbox-{}\" name=\"{}\" {} value=\"{}\" "
                        "class=\"mdc-checkbox__native-control\">",
                        checkbox_value, name, selected_html, checkbox_value),
            "<div class=\"mdc-checkbox__background\">",
            """
                    <svg version="1.1"
                        class="mdc-checkbox__checkmark"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        xml:space="preserve">
                    <path class="mdc-checkbox__checkmark__path"
                        fill="none"
                        stroke="white"
                        d="M1.73,12.91 8.1,19.28 22.79,4.59"/>
                    </svg>
                    """,
            "<div class=\"mdc-checkbox__mixedmark\"></div>",
            "</div>",
            "</div>",
            format_html("<label for=\"{}\">{}</label></div><br>", checkbox_value, force_text(checkbox_label))
        ]

        return "\n".join(output)

    def render_checkboxes(self, selected_choices, name):
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in self.choices:
            output.append(self.render_checkbox(selected_choices, option_value, option_label, name))
        return "\n".join(output)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, MultiValueDict):
            return data.getlist(name)
        return data.get(name)


class MaterialCheckboxInput(CheckboxInput):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type="checkbox", name=name)
        if self.check_test(value):
            final_attrs["checked"] = "checked"
        if not (value is True or value is False or value is None or value == ""):
            final_attrs["value"] = force_text(value)

        output = [
            "<br><div class=\"mdc-checkbox\" data-mdc-auto-init=\"MDCCheckbox\">",
            format_html("<input class=\"mdc-checkbox__native-control\" {}>", flatatt(final_attrs)),
            "<div class=\"mdc-checkbox__background\">",
            """
                    <svg version="1.1"
                        class="mdc-checkbox__checkmark"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        xml:space="preserve">
                    <path class="mdc-checkbox__checkmark__path"
                        fill="none"
                        stroke="white"
                        d="M1.73,12.91 8.1,19.28 22.79,4.59"/>
                    </svg>
                    """,
            "<div class=\"mdc-checkbox__mixedmark\"></div>",
            "</div></div>",
        ]

        # output = [
        #     "<div class=\"mdc-switch\">",
        #     format_html("<input class=\"mdc-checkbox__native-control\" {}>", flatatt(final_attrs)),
        #     "<div class=\"mdc-switch__background\">",
        #     "<div class=\"mdc-switch__knob\"></div>",
        #     "</div>",
        #     "</div></div>",
        # ]

        return "\n".join(output)

        # return format_html('<input{} />', flatatt(final_attrs))
