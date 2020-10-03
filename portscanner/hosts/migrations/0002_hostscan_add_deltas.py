# Generated by Django 3.1.1 on 2020-10-03 17:31

from django.db import migrations, models


def populate_deltas(apps, schema_editor):
    HostScan = apps.get_model('hosts', 'HostScan')
    scans = HostScan.objects.all().order_by('-created')
    count = 0
    for scan in scans:
        try:
            previous = [
                x
                for x in scans
                if x.created < scan.created and x.target == scan.target
            ][0]
        except IndexError:
            continue

        if opened := set(scan.ports["open"]) - set(previous.ports["open"]):
            scan.delta_opened = {'delta': list(opened)}
        if closed := set(previous.ports["open"]) - set(scan.ports["open"]):
            scan.delta_closed = {'delta': list(closed)}

        scan.save()
        count += 1
    print(f"Updated {count} scans")


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostscan',
            name='delta_closed',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='hostscan',
            name='delta_opened',
            field=models.JSONField(default=dict),
        ),
        migrations.RunPython(populate_deltas, reverse_code=migrations.RunPython.noop),
    ]




