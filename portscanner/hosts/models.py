from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy
from django_extensions.db.models import TimeStampedModel

from . import helpers


class Host(models.Model):
    # Hostname or IP
    label = models.CharField(max_length=200, unique=True)

    def save(self, run_scan=False, **kwargs):
        # Validate target
        if run_scan:
            if not helpers.validate_target(self.label):
                raise ValidationError("Invalid target, please resubmit.")

            # Execute Nmap scan
            if scan := helpers.scan_target(self.label):
                host, _ = Host.objects.get_or_create(label=self.label)
                hostscan = HostScan.objects.create(
                    target=host,
                    ports={"open": scan.get("open_ports", [])},
                    duration=scan["elapsed"],
                )
            else:
                raise ValidationError(f"Unable to nmap scan host target {target}")
        else:
            super().save(**kwargs)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse_lazy("portscanner.hosts:results", kwargs={"slug": self.label})


class HostScan(TimeStampedModel):
    target = models.ForeignKey(Host, on_delete=models.CASCADE)
    ports = models.JSONField()
    duration = models.PositiveIntegerField(default=0)
    delta_opened = models.JSONField(default=dict)
    delta_closed = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.target}: {self.created.ctime()}"

    @property
    def scan_time(self) -> str:
        return self.created.ctime()

    @property
    def changed(self) -> str:
        """
        Produce a string containing the opened and closed ports compared
        to the previous scan.
        """
        changed = ""
        if opened := self.delta_opened.get("delta"):
            changed += "Opened {}".format(" ".join(opened))
        if closed := self.delta_closed.get("delta"):
            if changed:
                changed += ", "
            changed += "Closed {}".format(" ".join(closed))

        return changed

    def save(self, **kwargs):
        scans = HostScan.objects.filter(target=self.target).order_by("-created")
        try:
            previous = scans[0]
            if opened := set(self.ports["open"]) - set(previous.ports["open"]):
                self.delta_opened = {"delta": list(opened)}
            if closed := set(previous.ports["open"]) - set(self.ports["open"]):
                self.delta_closed = {"delta": list(closed)}
        except IndexError:
            pass

        super().save(**kwargs)
