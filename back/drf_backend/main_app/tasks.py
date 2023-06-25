from drf_backend.celery import app

from data_app.models import ICAComponent
from .models import ICAImages, ICALinks, ICExtended, DatasetStats, CeleryLog


@app.task
def update_ic_plots(dataset_short_name: str) -> None:
    celery_log = CeleryLog(task='update-ic-plots', details=f'dataset: {dataset_short_name}')
    try:
        ics = ICAComponent.objects.all()
        if dataset_short_name:
            ics = ics.filter(dataset__short_name=dataset_short_name)

        for ic in ics:
            ic_x = ICExtended.get_or_create(ic.id)
            ic_x.update_plots()
        celery_log.success = True
    finally:
        celery_log.save()


@app.task
def update_links(dataset_short_name: str) -> None:
    celery_log = CeleryLog(task='update-links', details=f'dataset: {dataset_short_name}')
    try:
        ICExtended.update_links(dataset_short_name)
        celery_log.success = True
    finally:
        celery_log.save()


@app.task(name='update-dataset-stats')
def update_dataset_stats() -> None:
    celery_log = CeleryLog(task='update-dataset-stats')
    try:
        DatasetStats.update_stats()
        celery_log.success = True
    finally:
        celery_log.save()