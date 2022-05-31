from os.path import join

import pandas as pd
import numpy as np
import matplotlib

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.apps import apps

from .vis import plot_topomap, plot_epochs_image, plot_spectrum
from .models import Dataset, ICAComponent


app_path = apps.get_app_config('main_app').path


class VisTest(TestCase):
    def setUp(self):
        self.sfreq = 160.
        df_weights = pd.read_csv(join(app_path, 'test_data/ica_weights.csv'))
        df_data = pd.read_csv(join(app_path, 'test_data/ica_data.csv'))
        self.ica_component = df_weights['value'].values
        self.ch_names = df_weights['ch_name'].values
        self.df_data = df_data

    def test_topomap(self):
        fig = plot_topomap(self.ica_component, self.ch_names)
        self.assertEqual(matplotlib.figure.Figure == type(fig))

    def test_spectrum(self):
        fig = plot_spectrum(self.df_data, self.sfreq)
        self.assertEqual(matplotlib.figure.Figure == type(fig))

    def test_epochs_image(self):
        fig = plot_epochs_image(self.df_data)
        self.assertEqual(matplotlib.figure.Figure == type(fig))
