import os
import random
import json

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

from data_app.models import Annotation, Dataset, ICAComponent
from data_app.serializers import ICACreateSerializer


def init_test_db():
    # Create superuser
    User.objects.create_superuser('admin', 'admin@myproject.com', 'admin')
    admin = User.objects.get(username='admin')

    # Create test users
    user_1 = User(username='test_user_1')
    user_2 = User(username='test_user_2')
    user_1.save()
    user_2.save()

    # Create test dataset
    dataset = Dataset(short_name='test_dataset', full_name='Test dataset')
    dataset.save()

    dataset = Dataset(short_name='test_dataset_2', full_name='Test dataset 2')
    dataset.save()

    # Load ica data using serializer
    with open(os.path.join(settings.BASE_DIR, 'data_app/test_data/data_list.json')) as f:
        data_list = json.loads(f.read())
    for data_item in data_list:
        serializer = ICACreateSerializer(data=data_item)
        if serializer.is_valid():
            serializer.save()

    # Create random annotations
    ics = ICAComponent.objects.filter(dataset__short_name='test_dataset')
    for ic in ics:
        annotation = generate_random_annotation(ic, username='test_user_1')
        annotation.save()
        annotation = generate_random_annotation(ic, username='test_user_2')
        annotation.save()


def generate_random_annotation(ic=None, username=None):
    user = User.objects.get(username=username)
    obj = Annotation()
    obj.ic = ic
    obj.user = user

    flags = [
        'flag_brain',
        'flag_eyes',
        'flag_muscles'
    ]

    for flag in flags:
        if random.random() > 0.5:
            setattr(obj, flag, True)

    return obj
