from os.path import join

import pandas as pd
import numpy as np
import matplotlib

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.apps import apps

from data_app.models import Dataset, ICAComponent, Subject
from data_app.init_test_db import init_test_db
from django.contrib.auth.models import User


app_path = apps.get_app_config('data_app').path

EPS = 0.001


class ICAViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client.login(username='testuser', password='12345')
        Dataset.objects.create(full_name='My Dataset', short_name='my_dataset')

    def test_create(self):
        df_weights = pd.read_csv(join(app_path, 'test_data/ica_weights.csv'))
        df_data = pd.read_csv(join(app_path, 'test_data/ica_data.csv'))

        data = {
            "name": "IC0",
            "subject": "S1",
            "dataset": "my_dataset",
            "sfreq": 125.0,
            "data": {
                "ica_weights": df_weights.to_dict(orient='list'),
                "ica_data": df_data.to_dict(orient='list')
            }
        }

        response = self.client.post('/api/data/ic', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ic = ICAComponent.objects.get(id=response.data['id'])
        saved_ic_weights = ic.get_ica_weights()
        saved_ic_weights = saved_ic_weights[df_weights.columns]
        self.assertTrue(df_weights.equals(saved_ic_weights))


class SubjectTest(TestCase):
    def setUp(self):
        init_test_db()

    def test_get_components_data(self) -> None:
        ica_values, ica_epochs, sfreq = Subject.objects.first().get_components_data(60, 0)
        assert ica_values.shape == ica_epochs.shape
        assert abs(sfreq - 160) < EPS
        ica_values_2, ica_epochs_2, sfreq_2 = (
            Subject.objects.first().get_components_data(60, 0, use_decimate=True, decimate_min_sfreq=50)
        )
        assert abs(sfreq_2 - 80) < EPS
        assert ica_values_2.shape == ica_epochs_2.shape
        assert ica_values_2.shape[1] < ica_values.shape[1]

    def test_get_ic_names(self) -> None:
        ic_names = Subject.objects.first().get_ic_names()
        assert ic_names[0] == 'IC000'