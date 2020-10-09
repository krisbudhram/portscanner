from crispy_forms.helper import FormHelper
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

    def is_valid(self):
        try:
            self.instance = models.Host.objects.get(label=self.data.get("label"))
        except models.Host.DoesNotExist:
            return False

        return True
