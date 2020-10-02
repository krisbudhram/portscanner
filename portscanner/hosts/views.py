from django.contrib import messages
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
        form_kwargs = request.POST
        target = form_kwargs["target"]

        # Validate target
        if not helpers.validate_target(target):
            messages.error(request, "Invalid target, please resubmit.")
            return render(request, "hosts/hostscan.html", {"form": form})

        # Execute Nmap scan
        if scan := helpers.scan_target(target):
            host, _ = models.Host.objects.get_or_create(label=target)
            hostscan = models.HostScan.objects.create(
                target=host,
                ports={"open": scan.get("open_ports", [])},
                duration=scan["elapsed"],
            )

            return HttpResponseRedirect(
                reverse("portscanner.hosts:results", args=(host.label,))
            )
        else:
            messages.error(request, f"Unable to nmap scan host target {target}")
            return render(request, "hosts/hostscan.html", {"form": form})

    return render(request, "hosts/hostscan.html", {"form": form})


class ScanResults(FormMixin, ListView):
    form_class = forms.HostResultForm
    context_object_name = "hostscans"
    template_name = "hosts/results.html"
    queryset = (
        models.HostScan.objects.all().select_related("target").order_by("-created")
    )

    def get_context_data(self, **kwargs):
        if req_target := self.kwargs.get("req_target"):
            context = {"hostscans": self.queryset.filter(target__label=req_target)}
            if not context["hostscans"]:
                raise Http404
        else:
            context = {"hostscans": self.queryset.all()}

        # Make a list to pass into changed_ports, since filtering querysets would hit
        # the database each time.
        scanlist = list(self.queryset)
        for scan in context["hostscans"]:
            scan.changed = scan.changed_ports(scanlist)

        context.update(kwargs)
        return super().get_context_data(**context)

    def post(self, request, *args, **kwargs):
        host = self.get_form_kwargs().get("data").get("host", "")
        try:
            models.Host.objects.get(label=host)
        except models.Host.DoesNotExist:
            messages.error(request, f"No records for host {host}")
            return HttpResponseRedirect(reverse("portscanner.hosts:results"))

        return HttpResponseRedirect(reverse("portscanner.hosts:results", args=(host,)))
