import hashlib

import pandas as pd

from data_app.models import Dataset, ICAComponent, ICAData, Annotation


def _format_id(ic_id):
    return 'IC{:06d}'.format(ic_id)


def _hash_username(username):
    m = hashlib.sha256()
    m.update(username.encode())
    return m.hexdigest()


# create ics.csv
def create_ics(dataset_short_name):
    ics = ICAComponent.objects.filter(dataset__short_name=dataset_short_name)
    rows = []
    for ic in ics:
        rows.append((_format_id(ic.id), ic.sfreq))
    df_ics = pd.DataFrame(rows, columns=['ic_id', 'sfreq'])
    return df_ics


def create_annotations_raw(dataset_short_name):
    rows = []
    dataset = Dataset.objects.get(short_name=dataset_short_name)


    annotations = Annotation.objects.filter(ic__dataset__short_name=dataset_short_name)

    if dataset.annotation_version == 'v1':
        flags = [
            'flag_brain',
            'flag_alpha',
            'flag_mu',
            'flag_eyes',
            'flag_eyes_h',
            'flag_eyes_v',
            'flag_muscles',
            'flag_heart',
            'flag_line_noise',
            'flag_ch_noise',
        ]
    else:
        flags = [
            'flag_brain',
            'flag_alpha',
            'flag_mu',
            'flag_eyes',
            'flag_eyes_h',
            'flag_eyes_v',
            'flag_eyes_blinks',
            'flag_muscles_and_movement',
            'flag_muscles',
            'flag_movement',
            'flag_heart',
            'flag_noise',
            'flag_line_noise',
            'flag_ch_noise',
            'flag_uncertain',
            'flag_other',
        ]


    for a in annotations:
        d = {
            'ic_id': _format_id(a.ic.id),
            'user_hash': _hash_username(a.user.username),
            'comment': a.comment
        }
        for flag in flags:
            d[flag] = getattr(a, flag)

        rows.append(d)

    df_annotations_raw = pd.DataFrame(rows)
    return df_annotations_raw


def create_components_data_iter(dataset_short_name):
    ics = ICAComponent.objects.filter(dataset__short_name=dataset_short_name)
    for ic in ics:
        df_ica_weights = ic.get_ica_weights()
        df_ica_data = ic.get_ica_data()
        yield (_format_id(ic.id), df_ica_weights, df_ica_data)
