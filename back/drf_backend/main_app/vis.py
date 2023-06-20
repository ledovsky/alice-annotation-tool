import warnings

import matplotlib.pyplot as plt
import mne
import numpy as np
import plotly.express as px
from plotly import graph_objects as go


def _get_epochs_from_df(ica_data, sfreq):
    epochs = ica_data['epoch'].unique()
    n_epochs = len(epochs)
    counts = ica_data['epoch'].value_counts().values
    n_samples = counts[0]
    assert np.all(counts == n_samples) == True

    np_data = np.empty((n_epochs, 1, n_samples))

    for idx, epoch in enumerate(epochs):
        np_data[idx, 0, :] = ica_data[ica_data['epoch'] == epoch]['value'].values

    info = mne.io.meas_info.create_info(['ICA000'], sfreq=sfreq, ch_types="misc")

    epochs_from_df = mne.EpochsArray(np_data, info)

    return epochs_from_df


def plot_epochs_image(ica_data, sfreq):
    with warnings.catch_warnings():  # mean of empty slice
        warnings.simplefilter('ignore')
        epochs_from_df = _get_epochs_from_df(ica_data, sfreq)
        return mne.viz.epochs.plot_epochs_image(epochs_from_df, picks=[0], title="",
                                                combine=None, colorbar=False, show=False)[0]


def plot_topomap(ica_component, ch_names):

    with warnings.catch_warnings():  # mean of empty slice
        warnings.simplefilter('ignore')
        fig, ax = plt.subplots()

        head_pos = None
        outlines = 'head'

        res = 64
        contours = 6
        sensors = True
        image_interp = 'bilinear'
        show = True
        extrapolate = 'box'
        head_pos = None
        border = 0

        # channels_to_use = [ch.lower() for ch in ica_epochs.info['ch_names']]
        channels_to_use = ch_names

        ten_twenty_montage = mne.channels.make_standard_montage('standard_1020')

        # get channels in format of ten_twenty_montage in right order
        ten_twenty_montage_channels = {ch.lower(): ch for ch in ten_twenty_montage.ch_names}
        channels_to_use_ = [ten_twenty_montage_channels[ch] for ch in channels_to_use]

        # create Info object to store info
        info = mne.io.meas_info.create_info(channels_to_use_, sfreq=256, ch_types="eeg")

        # using temporary RawArray to apply mongage to info
        mne.io.RawArray(np.zeros((len(channels_to_use_), 1)), info, copy=None).set_montage(ten_twenty_montage)

        # pick channels
        channels_to_use_ = [ch for ch in info.ch_names if ch.lower() in channels_to_use]
        info.pick_channels(channels_to_use_)

        data_picks, pos, merge_channels, names, _, sphere, clip_origin = mne.viz.topomap._prepare_topomap_plot(info, 'eeg')

        outlines = mne.viz.topomap._make_head_outlines(sphere, pos, outlines, clip_origin)

        mne.viz.topomap.plot_topomap(
            ica_component.ravel(), pos, res=res,
            outlines=outlines, contours=contours, sensors=sensors,
            image_interp=image_interp, show=show, extrapolate=extrapolate,
            sphere=sphere, border=border, axes=ax
        )

    return fig


def plot_spectrum(ica_data, sfreq):
    def _get_psd_label_and_std(this_psd, dB, num_std):
        """Handle setting up PSD for one component, for plot_ica_properties."""
        psd_ylabel = mne.viz.ica._convert_psds(this_psd, dB, estimate='auto', scaling=1.,
                                               unit='AU', first_dim='epoch')
        psds_mean = this_psd.mean(axis=0)
        diffs = this_psd - psds_mean
        # the distribution of power for each frequency bin is highly
        # skewed so we calculate std for values below and above average
        # separately - this is used for fill_between shade
        with warnings.catch_warnings():  # mean of empty slice
            warnings.simplefilter('ignore')
            spectrum_std = [
                [np.sqrt((d[d < 0] ** 2).mean(axis=0)) for d in diffs.T],
                [np.sqrt((d[d > 0] ** 2).mean(axis=0)) for d in diffs.T]]
        spectrum_std = np.array(spectrum_std) * num_std

        return psd_ylabel, psds_mean, spectrum_std


    def set_title_and_labels(ax, xlab, ylab):
        if xlab:
            ax.set_xlabel(xlab)
        if ylab:
            ax.set_ylabel(ylab)
        ax.axis('auto')
        ax.tick_params('both', labelsize=8)
        ax.axis('tight')

    epochs_from_df = _get_epochs_from_df(ica_data, sfreq)

    # Params
    Nyquist = sfreq / 2.
    dB = True
    plot_std = True
    num_std = 1
    psd_args = {}
    psd_args['fmax'] = 75

    psds, freqs = mne.time_frequency.psd_multitaper(epochs_from_df, picks=[0], **psd_args)
    psd_ylabel, psds_mean, spectrum_std = _get_psd_label_and_std(
        psds[:, 0, :].copy(), dB, num_std)

    fig, spec_ax = plt.subplots()

    spec_ax.plot(freqs, psds_mean, color='k')
    if plot_std:
        spec_ax.fill_between(freqs, psds_mean - spectrum_std[0],
                             psds_mean + spectrum_std[1],
                             color='k', alpha=.2)

    set_title_and_labels(spec_ax, 'Frequency (Hz)', psd_ylabel)
    spec_ax.yaxis.labelpad = 0
    spec_ax.set_xlim(freqs[[0, -1]])
    ylim = spec_ax.get_ylim()
    air = np.diff(ylim)[0] * 0.1
    spec_ax.set_ylim(ylim[0] - air, ylim[1] + air)

    return fig


def plot_components(ica_values, ica_epochs, ic_names, sfreq):
    """
    Inspired by https://plotly.com/python/range-slider/
    """

    palette = px.colors.qualitative.Plotly

    # define time when epoch changes
    epoch_change_time = []
    for idx, epoch_id, epoch_id_prev in zip(
            np.arange(ica_values.shape[1]),
            ica_epochs[0, 1:],
            ica_epochs[0, :]):
        if epoch_id != epoch_id_prev:
            epoch_change_time.append(idx / sfreq)

    fig = go.Figure()

    fig.update_layout({'showlegend': False})

    n_components = ica_values.shape[0]
    step = 1 / n_components

    fig.update_layout({
        f'xaxis': {
            'range': [0, 15],
            'rangeslider': {
                'visible': True,
                'autorange': True
            }
        }
    })

    for t in epoch_change_time:
        fig.add_shape(
            type="line",
            x0=t, x1=t, y0=0, y1=1,
            xref='x',
            yref=f'paper',
            line=dict(color=palette[1], width=1.5))

    time = np.arange(ica_values.shape[1]) / sfreq
    for ic_idx, col_name in enumerate(reversed(ic_names)):
        axis_idx = ic_idx + 1
        fig.update_layout({f'yaxis{axis_idx}': {
            'anchor': 'x',
            'domain': [ic_idx * step, (ic_idx + 1) * step],
            'showticklabels': False,
            'zeroline': False
        }})

        fig.add_trace(
            go.Scatter(
                x=time,
                y=ica_values[n_components - ic_idx - 1, :],
                yaxis=f'y{ic_idx + 1}',
                name=col_name,
                mode='lines',
                line=dict(color='royalblue', width=1),
                hovertemplate='IC value: %{y:.2f}<br>Time:%{x:.2f}',
            )
        )

        fig.add_annotation(x=-0.06, y=0,
                           xref='paper', yref=f'y{ic_idx + 1}',
                           text=col_name,
                           showarrow=False,
                           yshift=0)

    # Update layout
    fig.update_layout({
        'dragmode': 'zoom',
        'height': 40 * n_components,
        'template': 'plotly_white',
        'margin': {
            't': 10,
            'b': 10,
            'r': 10,
        },
    })

    return fig
