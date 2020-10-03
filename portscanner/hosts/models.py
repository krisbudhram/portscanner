from django.db import models
from django_extensions.db.models import TimeStampedModel


class Host(models.Model):
    # Hostname or IP
    label = models.CharField(max_length=200)

    def __str__(self):
        return self.label


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
