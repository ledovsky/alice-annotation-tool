from django.db import models


class BackgroundTask(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    task = models.CharField(max_length=128, null=False)
    status = models.CharField(
        max_length=128,
        choices=(('in progress', 'in progress'), ('success', 'success'), ('failed', 'failed'))
    )
    dttm = models.DateTimeField(auto_now=True)
    details = models.TextField(null=True)