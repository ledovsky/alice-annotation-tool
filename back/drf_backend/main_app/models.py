import io
import json
from collections import OrderedDict

import matplotlib.pyplot as plt

from django.db import models
from django.core.files.base import ContentFile

from main_app.vis import plot_topomap, plot_epochs_image, plot_spectrum, plot_sources

from data_app.models import Dataset, ICAComponent, Annotation, ICAData


class ICAImages(models.Model):
    ic = models.OneToOneField(ICAComponent, null=False, related_name='images', on_delete=models.CASCADE)
    img_topomap = models.ImageField(upload_to='images/', null=True)
    img_spectrum = models.ImageField(upload_to='images/', null=True)
    img_epochs_image = models.ImageField(upload_to='images/', null=True)
    img_sources_plot = models.JSONField(null=True)

    def build_plots(self):
        df_weights = self.ic.get_ica_weights()
        df_data = self.ic.get_ica_data()

        fig = plot_topomap(df_weights['value'].values, df_weights['ch_name'].values)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=200, bbox_inches='tight', transparent=True)
        plt.close(fig)
        self.img_topomap.save('topomap.png', ContentFile(buf.getvalue()))

        fig = plot_spectrum(df_data, self.ic.sfreq)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=200, bbox_inches='tight', transparent=True)
        plt.close(fig)
        self.img_spectrum.save('spectrum.png', ContentFile(buf.getvalue()))

        fig = plot_epochs_image(df_data, self.ic.sfreq)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=200, bbox_inches='tight', transparent=True)
        plt.close(fig)
        self.img_epochs_image.save('epochs_image.png', ContentFile(buf.getvalue()))

        self.save()

    def build_component_plots(self):

        ic_objs = (
            ICAComponent
                .objects
                .filter(dataset=self.ic.dataset, subject=self.ic.subject)
                .order_by('name')
        )
        ics = OrderedDict()
        for ic_obj in ic_objs:
            ica_data_obj = ICAData.objects.get(ic=ic_obj)
            ica_data = json.loads(ica_data_obj.ica_data)
            del ica_data_obj
            sfreq = ic_obj.sfreq
            while sfreq > 100:
                sfreq /= 2
                ica_data['value'] = ica_data['value'][::2]
                ica_data['epoch'] = ica_data['epoch'][::2]
            ica_data['value'] = ica_data['value'][:1000]
            ica_data['epoch'] = ica_data['epoch'][:1000]
            ics[ic_obj.name] = ica_data

        fig = plot_sources(ics, sfreq)
        self.img_sources_plot = json.loads(fig.to_json())

        self.save()

    @staticmethod
    def update_plots(dataset_short_name=None):
        ics = ICAComponent.objects.all()
        if dataset_short_name:
            ics = ics.filter(dataset__short_name=dataset_short_name)

        for ic in ics:
            if not hasattr(ic, 'images'):
                ic_img = ICAImages(ic=ic)
                ic_img.save()
            else:
                ic_img = ic.images
            ic_img.build_plots()

    @staticmethod
    def update_component_plots(dataset_short_name=None):
        ics = ICAComponent.objects.all()
        if dataset_short_name:
            ics = ics.filter(dataset__short_name=dataset_short_name)

        for ic in ics:
            if not hasattr(ic, 'images'):
                ic_img = ICAImages(ic=ic)
                ic_img.save()
            else:
                ic_img = ic.images
            ic_img.build_component_plots()


class ICALinks(models.Model):
    ic = models.OneToOneField(ICAComponent, null=False, on_delete=models.CASCADE, related_name='links')
    prev = models.OneToOneField(ICAComponent, null=True, on_delete=models.SET_NULL, related_name='link_from_next')
    next = models.OneToOneField(ICAComponent, null=True, on_delete=models.SET_NULL, related_name='link_from_prev')

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
