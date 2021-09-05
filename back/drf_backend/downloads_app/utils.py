def _get_base_name(dataset, version=None):
    s = 'dataset_' + dataset
    if version:
        s += '_' + version
    return s

def get_dirname(dataset, version=None):
    return _get_base_name(dataset, version)

def get_archive_name(dataset, version=None):
    return _get_base_name(dataset, version) + '.zip'