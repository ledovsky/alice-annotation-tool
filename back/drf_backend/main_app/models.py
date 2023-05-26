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

    @staticmethod
    def build_component_plots(dataset_short_name, subject):

        ic_objs = (
            ICAComponent
                .objects
                .filter(dataset__short_name=dataset_short_name, subject=subject)
                .order_by('name')
        )

        ics = OrderedDict()

        sfreq = None
        for ic_obj in ic_objs.iterator(chunk_size=1):
            ica_data_obj = ICAData.objects.get(ic=ic_obj)
            ica_data = json.loads(ica_data_obj.ica_data)
            sfreq = ic_obj.sfreq
            del ica_data_obj

            # select 30 seconds
            n_points_to_take = int(sfreq * 30)
            ica_data['value'] = ica_data['value'][:n_points_to_take]
            ica_data['epoch'] = ica_data['epoch'][:n_points_to_take]

            # lower resulotion to 60-120Hz
            while sfreq >= 120:
                sfreq /= 2
                ica_data['value'] = ica_data['value'][::2]
                ica_data['epoch'] = ica_data['epoch'][::2]

            ics[ic_obj.name] = ica_data

        if len(ics) == 0:
            raise RuntimeError('No ics in dataset')

        fig = plot_sources(ics, sfreq)
        for ic_obj in ic_objs.iterator(chunk_size=1):
            if not hasattr(ic_obj, 'images'):
                ic_img = ICAImages(ic=ic_obj)
                ic_img.save()
            ic_obj.images.img_sources_plot = json.loads(fig.to_json())
            ic_obj.images.save()

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

        # TODO: need testing
        if dataset_short_name is None:

            raise NotImplementedError

            query = Dataset.objects.all().values_list('short_name').distinct()
            datasets = [item[0] for item in list(query)]
            for dataset in datasets:
                ICAImages.update_component_plots(dataset)
            return

        ics = ICAComponent.objects.filter(dataset__short_name=dataset_short_name)


        query = ics.values_list('subject').distinct()
        subjects = [item[0] for item in list(query)]

        for subj in subjects:
            ICAImages.build_component_plots(dataset_short_name, subj)


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
