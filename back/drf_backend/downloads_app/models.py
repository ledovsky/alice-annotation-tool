from django.db import models

from data_app.models import Dataset


class DatasetDownloadItem(models.Model):
    dataset = models.ForeignKey(Dataset, models.PROTECT)
    is_actual = models.BooleanField(default=False)
    file = models.FileField(upload_to='downloads')
    version = models.CharField(max_length=128, default='NA')
    uploaded_dt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('dataset', 'version')