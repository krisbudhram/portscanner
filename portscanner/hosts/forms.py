from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from . import models


class HostScanForm(forms.ModelForm):
    """
    Scan tab 'Scan' form
    """

    class Meta:
        model = models.Host
        fields = ["label"]
        labels = {"label": "Host"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"
        self.helper.add_input(
            Submit("submit", "Scan", css_id="bt", css_class="btn btn-success w-25")
        )
        self.helper.layout = Layout(
            "label",
        )

    def save(self, run_scan=True, **kwargs):
        try:
            host = models.Host.objects.get(label=self.data["label"])
        except models.Host.DoesNotExist:
            host = models.Host()
            host.label = self.data["label"]

        host.save(run_scan=run_scan)

    def is_valid(self):
        return bool(self.data.get("label", False))


class HostResultForm(forms.ModelForm):
    """
    Result tab 'Search' form
    """

    class Meta:
        model = models.Host
        fields = ["label"]
        labels = {"label": "Host"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"
        self.helper.add_input(
            Submit("submit", "Search", css_class="btn btn-success w-25")
        )
        self.helper.layout = Layout(
            "label",
        )

    def is_valid(self):
        try:
            self.instance = models.Host.objects.get(label=self.data.get("label"))
        except models.Host.DoesNotExist:
            return False

        return True
