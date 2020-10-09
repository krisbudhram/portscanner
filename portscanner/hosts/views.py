from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.views.generic import CreateView, ListView
from django.views.generic.edit import FormMixin

from . import forms, helpers, models


def hostscan(request):
    form = forms.HostScanForm

    if request.method == "POST":
        form = forms.HostScanForm(request.POST)

        if form.is_valid():
            try:
                form.save(run_scan=True)
            except ValidationError as e:
                messages.error(request, f"Error: {e.message}")
                return render(request, "hosts/hostscan.html", {"form": form})

            return HttpResponseRedirect(
                reverse("portscanner.hosts:results", args=(form.data["label"],))
            )
        else:
            messages.error(request, f"Error: Invalid form submission")

    return render(request, "hosts/hostscan.html", {"form": form})


class ScanResults(FormMixin, ListView):
    form_class = forms.HostResultForm
    context_object_name = "hostscans"
    template_name = "hosts/results.html"
    queryset = (
        models.HostScan.objects.all().select_related("target").order_by("-created")
    )

    def get_context_data(self, **kwargs):
        if slug := self.kwargs.get("slug"):
            context = {"hostscans": self.queryset.filter(target__label=slug)}
            if not context["hostscans"]:
                raise Http404
        else:
            context = {"hostscans": self.queryset.all()}

        context.update(kwargs)
        return super().get_context_data(**context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return HttpResponseRedirect(form.instance.get_absolute_url())
        else:
            messages.error(request, f"No records for host")

        return HttpResponseRedirect(request.path_info)
