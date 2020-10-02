from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms

from . import models


class HostScanForm(forms.Form):
    """
    Scan tab 'Scan' form
    """
    target = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HostResultForm(forms.Form):
    """
    Result tab 'Search' form
    """
    host = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
