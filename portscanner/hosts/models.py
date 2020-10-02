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

    def __str__(self):
        return f"{self.target}: {self.created.ctime()}"

    @property
    def scan_time(self) -> str:
        return self.created.ctime()

    def changed_ports(self, scanlist: list) -> str:
        changed = ""
        try:
            # Since scanlist is already ordered by created, just pick the first element
            previous = [
                x
                for x in scanlist
                if x.created < self.created and x.target == self.target
            ][0]
        except IndexError:
            return changed

        if opened := set(self.ports["open"]) - set(previous.ports["open"]):
            changed += "Opened {}".format(" ".join(port for port in opened))

        if closed := set(previous.ports["open"]) - set(self.ports["open"]):
            if changed:
                changed += ", "
            changed += "Closed {}".format(" ".join(port for port in closed))

        return changed
