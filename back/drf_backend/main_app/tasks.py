from drf_backend.celery import app

from data_app.models import ICAComponent
from .models import ICAImages, ICALinks, ICExtended


@app.task
def recalc_dataset(dataset_short_name):
    ICALinks.update_links(dataset_short_name)
    ICAImages.update_plots(dataset_short_name)


@app.task
def update_ic_plots(dataset_short_name: str) -> None:
    ics = ICAComponent.objects.all()
    if dataset_short_name:
        ics = ics.filter(dataset__short_name=dataset_short_name)

    for ic in ics:
        ic_x = ICExtended.get_or_create(ic.id)
        ic_x.update_plots()


@app.task
def update_links(dataset_short_name: str) -> None:
    ICExtended.update_links(dataset_short_name)