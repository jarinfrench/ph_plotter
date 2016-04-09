#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

__author__ = "Yuji Ikeda"

import numpy as np
from matplotlib.ticker import AutoMinorLocator
from .plotter import Plotter, read_band_labels


def read_band_yaml(yaml_file="band.yaml"):
    import yaml
    data = yaml.load(open(yaml_file, "r"))
    nqpoint = data['nqpoint']
    npath = data['npath']
    natom = data['natom']
    nband = natom * 3
    nsep = nqpoint // npath
    distance = np.zeros((npath, nsep))
    frequency = np.zeros((npath, nsep, nband))
    for ipath in range(npath):
        for isep in range(nsep):
            iq = ipath * nsep + isep
            distance[ipath, isep] = data['phonon'][iq]['distance']
            for iband in range(nband):
                frequency[ipath, isep, iband] = (
                    data['phonon'][iq]['band'][iband]['frequency']
                )
    return distance, frequency


class BandPlotter(Plotter):
    def load_data(self, data_file="band.yaml"):
        print("Reading band.yaml: ", end="")
        distances, frequencies = read_band_yaml(yaml_file=data_file)
        print("Finished")

        self._distances = distances
        self._frequencies = frequencies

        band_labels = read_band_labels("band.conf")
        print("band_labels:", band_labels)
        self._band_labels = band_labels

        return self

    def plot(self, ax):
        variables = self._variables

        distances = self._distances
        frequencies = self._frequencies

        freq_label = "Frequency ({})".format(variables["freq_unit"])
        d_freq = variables["d_freq"]
        f_min = variables["f_min"]
        f_max = variables["f_max"]
        n_freq = int((f_max - f_min) / d_freq) + 1

        ml = AutoMinorLocator(2)
        ax.yaxis.set_minor_locator(ml)

        ax.set_xticks([0.0] + list(distances[:, -1]))
        ax.set_xticklabels(self._band_labels)
        ax.set_xlabel("Wave vector")
        ax.set_xlim(distances[0, 0], distances[-1, -1])

        ax.set_yticks(np.linspace(f_min, f_max, n_freq))
        ax.set_ylabel(freq_label)
        ax.set_ylim(f_min, f_max)

        for x in [0.0] + list(distances[:, -1]):
            ax.axvline(x, color="k", dashes=(2, 2), linewidth=0.5)
        # for y in np.linspace(f_min, f_max, n_freq):
        #     plt.axhline(y, color="#000000", linestyle=":")
        ax.axhline(0, color="k", dashes=(2, 2), linewidth=0.5)  # zero axis

        npath, nqpoint, nband = frequencies.shape
        for ipath in range(npath):
            lines = ax.plot(
                distances[ipath],
                frequencies[ipath] * variables["unit"],
                variables["linecolor"],
                dashes=variables["dashes"],
                linewidth=variables["linewidth"],
            )

    def create_figure_name(self):
        variables = self._variables
        figure_name = "band_{}.{}".format(
            variables["freq_unit"],
            variables["figure_type"])
        return figure_name
