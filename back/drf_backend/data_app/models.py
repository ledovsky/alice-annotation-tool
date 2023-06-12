from collections import OrderedDict
import json
import pandas as pd
from typing import List, Tuple

import numpy as np
from scipy.signal import decimate

from django.contrib.auth.models import User
from django.db import models


class Dataset(models.Model):
    short_name = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=128)
    description = models.TextField(default='No description available')
    locked = models.BooleanField(unique=False, default=False)
    annotation_version = models.CharField(max_length=128, choices=[('v1', 'v1'), ('v2', 'v2')], default='v1')

    def reset(self):
        if not self.locked:
            ics = self.ics.all()
            ics.delete()
        else:
            raise Exception('Model is locked')
    
    def __str__(self):
        return f'Dataset {self.short_name}'


class Subject(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='subjects', on_delete=models.PROTECT)
    name = models.CharField(max_length=128)

    class Meta:
        unique_together = ('dataset', 'name')
    
    def __str__(self) -> str:
        return f'Subject {self.name} {self.dataset.short_name}'
    
    def get_components_data(
            self, n_seconds: int = None, offset_seconds: int = None, use_decimate: bool = False, 
            decimate_min_sfreq=50) -> Tuple[np.ndarray, np.ndarray, float]:
        """Returns ICA data points for the subject
        Allows taking of the subsample and decimation

        Returns:
            ica_values: n_components x n_values
            ica_epochs: n_components x n_values - epoch idx of each sample
            sfreq: sampling frequency
        """
        ic_objs = (
            ICAComponent
                .objects
                .filter(subject=self)
                .order_by('name')
        )

        n_components = len(ic_objs)
        if n_components == 0:
            return None, None
        
        
        ica_values = None
        ica_epochs = None
        sfreq = None

        for idx, ic_obj in enumerate(ic_objs.iterator(chunk_size=1)):
            ica_data_obj = ICAData.objects.get(ic=ic_obj)
            ica_data = json.loads(ica_data_obj.ica_data)
            if ica_values is None:
                ica_values = np.empty(shape=(n_components, len(ica_data['value'])), dtype=np.float64)
                ica_epochs = np.empty(shape=(n_components, len(ica_data['value'])), dtype=np.int64)
            if sfreq is None:
                sfreq = ic_obj.sfreq


            ica_values[idx, :] = ica_data['value']
            ica_epochs[idx, :] = ica_data['epoch']

            del ica_data_obj
            del ica_data
        
        if offset_seconds:
            ica_values = ica_values[:, int(offset_seconds * sfreq) :]
            ica_epochs = ica_epochs[:, int(offset_seconds * sfreq) :]
        if n_seconds:
            ica_values = ica_values[:, : int(n_seconds * sfreq)]
            ica_epochs = ica_epochs[:, : int(n_seconds * sfreq)]

        if use_decimate:
            q = 1
            while sfreq >= decimate_min_sfreq * 2:
                sfreq /= 2
                q *= 2
                ica_values = decimate(ica_values, q=q, axis=1)
                ica_epochs = ica_epochs[:, ::q]

        return ica_values, ica_epochs, sfreq
    
    def get_ic_names(self) -> List[str]:
        """Returns component names in ascending order"""
        ic_objs = (
            ICAComponent
                .objects
                .filter(subject=self)
                .order_by('name')
        )
        return [ic.name for ic in ic_objs]


class ICAData(models.Model):
    ica_weights = models.TextField()
    ica_data = models.TextField()

    def __str__(self):
        if hasattr(self, 'ic'):
            return f'ICAData {self.ic.__str__()}'
        else:
            return f'ICAData {self.id}'


class ICAComponent(models.Model):
    name = models.CharField(max_length=128)
    subject_name = models.CharField(max_length=128)
    subject = models.ForeignKey(Subject, null=True, related_name='ics', on_delete=models.SET_NULL)
    dataset = models.ForeignKey(Dataset, related_name='ics', on_delete=models.PROTECT)
    sfreq = models.FloatField()
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    data_obj = models.OneToOneField(ICAData, null=False, related_name='ic', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'subject_name', 'dataset')

    def get_ica_weights(self):
        return pd.DataFrame(json.loads(ICAData.objects.get(ic=self).ica_weights))

    def get_ica_data(self):
        return pd.DataFrame(json.loads(ICAData.objects.get(ic=self).ica_data))
    
    def __str__(self):
        return f'ICComponent {self.name} {self.subject} {self.dataset.short_name}'


class Annotation(models.Model):
    ic = models.ForeignKey(ICAComponent, models.PROTECT)
    user = models.ForeignKey(User, models.PROTECT)
    flag_brain = models.BooleanField(default=False)
    flag_eyes = models.BooleanField(default=False)
    flag_eyes_blinks = models.BooleanField(default=False)
    flag_eyes_h = models.BooleanField(default=False)
    flag_eyes_v = models.BooleanField(default=False)
    flag_muscles_and_movement = models.BooleanField(default=False)
    flag_muscles = models.BooleanField(default=False)
    flag_movement = models.BooleanField(default=False)
    flag_heart = models.BooleanField(default=False)
    flag_noise = models.BooleanField(default=False)
    flag_line_noise = models.BooleanField(default=False)
    flag_ch_noise = models.BooleanField(default=False)
    flag_uncertain = models.BooleanField(default=False)
    flag_other = models.BooleanField(default=False)
    flag_mu = models.BooleanField(default=False)
    flag_alpha = models.BooleanField(default=False)
    comment = models.TextField(default='', blank=True)
    updated_dt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('ic', 'user', )
