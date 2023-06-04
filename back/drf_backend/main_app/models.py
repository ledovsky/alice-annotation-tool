import json
import os
from os.path import join
from collections import OrderedDict
from typing import TypeVar, Type

import matplotlib.pyplot as plt

from django.db import models
from django.core.files.base import ContentFile
from django.conf import settings

from data_app.models import Dataset, ICAComponent, Annotation, ICAData
from main_app.vis import plot_topomap, plot_spectrum, plot_epochs_image


# Create a generic variable that can be 'Parent', or any subclass.
T = TypeVar('T', bound='Parent')


class ICAImages(models.Model):
    ic = models.OneToOneField(ICAComponent, null=False, related_name='images', on_delete=models.CASCADE)
    img_topomap = models.ImageField(upload_to='images/', null=True)
    img_spectrum = models.ImageField(upload_to='images/', null=True)
    img_epochs_image = models.ImageField(upload_to='images/', null=True)
    img_sources_plot = models.JSONField(null=True)

    @staticmethod
    def update_plots(dataset_short_name=None):
        ics = ICAComponent.objects.all()
        if dataset_short_name:
            ics = ics.filter(dataset__short_name=dataset_short_name)

        for ic in ics:
            ic_x = ICExtended.get_or_create(ic.id)

            save_opts = dict(format='png', dpi=200, bbox_inches='tight', transparent=True)

            df_weights = ic.get_ica_weights()
            df_data = ic.get_ica_data()

            fig = plot_topomap(df_weights['value'].values, df_weights['ch_name'].values)
            fig.savefig(ic_x.get_image_path('topomap', create_dir=True), **save_opts)
            plt.close(fig)

            fig = plot_spectrum(df_data, ic.sfreq)
            fig.savefig(ic_x.get_image_path('spectrum', create_dir=True), **save_opts)
            plt.close(fig)

            fig = plot_epochs_image(df_data, ic.sfreq)
            fig.savefig(ic_x.get_image_path('epochs_image', create_dir=True), **save_opts)
            plt.close(fig)

            ic_x.img_ready = True


class ICALinks(models.Model):
    ic = models.OneToOneField(ICAComponent, null=False, on_delete=models.CASCADE, related_name='links')
    prev = models.OneToOneField(ICAComponent, null=True, on_delete=models.SET_NULL, related_name='link_from_next_old')
    next = models.OneToOneField(ICAComponent, null=True, on_delete=models.SET_NULL, related_name='link_from_prev_old')

    @staticmethod
    def update_links(dataset_short_name):
        ics = ICAComponent.objects.filter(dataset__short_name=dataset_short_name).order_by('subject', 'name')
        prev = None
        for ic in ics:
            if not hasattr(ic, 'links'):
                links = ICALinks(ic=ic)
                links.save()
            if prev is not None:
                links = ic.links
                links.prev = prev
                links.save()
                links = prev.links
                links.next = ic
                links.save()
            prev = ic


class ICExtended(models.Model):
    ic = models.OneToOneField(ICAComponent, null=False, on_delete=models.CASCADE, related_name='x')
    img_ready = models.BooleanField(default=False)
    prev = models.OneToOneField(ICAComponent, null=True, on_delete=models.SET_NULL, related_name='link_from_next')
    next = models.OneToOneField(ICAComponent, null=True, on_delete=models.SET_NULL, related_name='link_from_prev')

    @staticmethod
    def update_links(dataset_short_name: str) -> None:
        ics = ICAComponent.objects.filter(dataset__short_name=dataset_short_name).order_by('subject', 'name')
        prev = None
        for ic in ics:
            if not hasattr(ic, 'links'):
                links = ICALinks(ic=ic)
                links.save()
            if prev is not None:
                links = ic.links
                links.prev = prev
                links.save()
                links = prev.links
                links.next = ic
                links.save()
            prev = ic
    
    @classmethod
    def get_or_create(cls: Type[T], ic_id: int) -> T:
        ic_x = None
        try:
            ic_x = cls.objects.get(ic=ic_id)
        except cls.DoesNotExist:
            ic = ICAComponent.objects.get(id=ic_id)
            ic_x = cls(ic=ic)
            ic_x.save()
        return ic_x
    
    def get_image_dir(self, image_type: str, create: bool = False) -> str:
        subject = self.ic.subject
        dataset = subject.dataset
        path = join(settings.MEDIA_ROOT, image_type, dataset.short_name, subject.name)
        if create:
            os.makedirs(path, exist_ok=True)
        return path

    def get_image_path(self, t: str, create_dir: bool = False) -> str:
        return join(self.get_image_dir(t, create=create_dir), self.ic.name + '.png')



class DatasetStats(models.Model):
    dataset = models.OneToOneField(Dataset, related_name='stats', on_delete=models.CASCADE)
    n_components = models.IntegerField(default=0)
    agreement = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'DatasetStats'

    @staticmethod
    def update_stats():
        datasets = Dataset.objects.all()
        for dataset in datasets:
            if not hasattr(dataset, 'stats'):
                stat_obj = DatasetStats(dataset=dataset)
                stat_obj.save()
        stats = DatasetStats.objects.all()
        for stat_obj in stats:
            n_components = 0
            if hasattr(stat_obj.dataset, 'ics'):
                n_components = len(stat_obj.dataset.ics.all())
            stat_obj.n_components = n_components
            stat_obj.save()
