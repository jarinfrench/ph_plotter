#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os

import h5py
import numpy as np

from ph_plotter.plotter import Plotter, read_band_labels

__author__ = "Yuji Ikeda"


def convert_binary2string(x):
    """x: numpy.array"""
    if isinstance(x, np.ndarray) and x.shape != ():
        return [convert_binary2string(_) for _ in x]
    else:
        # The "bytes" function is necessary because
        # numpy.bytes_ does not have the decode method.
        return bytes(x).decode("ascii")


class SFPlotter(Plotter):
    def load_data(self, data_file="sf.hdf5"):
        _, extension = os.path.splitext(data_file)
        if extension == ".hdf5":
            self.load_data_hdf5(data_file)
        else:
            self.load_data_text(data_file)
        print("Finished")

        band_labels = read_band_labels("/".join([self._variables["dir"], "band.conf"]))
        print("band_labels:", band_labels)
        self._band_labels = band_labels

    def load_data_hdf5(self, data_file="sf.hdf5"):
        with h5py.File(data_file, "r") as data:
            paths = np.array(data["paths"])
            npaths, npoints = paths.shape[:2]

            frequencies = np.array(data["frequencies"])
            self._is_squared = np.array(data["is_squared"])

            keys = [
                "natoms_primitive",
                "elements",
                "distance",
                "pointgroup_symbol",
                "num_irreps",
                "ir_labels",
                "total_sf",
                "partial_sf_s",
                "partial_sf_e",
                "partial_sf_s_e",
                "partial_sf_e2",
            ]
            data_points = []
            distances = []
            for ipath in range(npaths):
                distances_on_path = []
                for ip in range(npoints):
                    group = "{}/{}/".format(ipath, ip)
                    data_points.append(
                        {
                            k: np.array(data[group + k])
                            for k in keys
                            if group + k in data
                        }
                    )

                    distances_on_path.append(np.array(data[group + "distance"]))
                distances.append(distances_on_path)

            data_points = [self.convert_binary2string(d) for d in data_points]
            self._data_points = data_points
            self._distances = np.array(distances)

        xs = self._distances.reshape(-1) / np.nanmax(self._distances)
        self._frequencies, self._xs = np.meshgrid(frequencies, xs)

    @staticmethod
    def convert_binary2string(data_point):
        keys = ["elements", "pointgroup_symbol", "ir_labels"]
        for key in keys:
            data_point[key] = convert_binary2string(data_point[key])
        return data_point

    def load_data_text(self, data_file):
        data = np.loadtxt(data_file, usecols=(0, 1, 2)).T
        nfreq = len(np.unique(data[1]))
        xs = data[0].reshape(-1, nfreq)
        self._frequencies = data[1].reshape(-1, nfreq)
        total_sf = data[2].reshape(-1, nfreq)
        data_points = []
        for total_sf_point in total_sf:
            data_points.append({"total_sf": total_sf_point})
        self._data_points = data_points

        distances = xs[:, 0]
        npaths = len(distances) - len(np.unique(distances)) + 1
        self._distances = distances.reshape(npaths, -1)

        self._xs = xs / np.nanmax(self._distances)

        self._is_squared = self._check_is_squared(data_file)

    @staticmethod
    def _check_is_squared(filename):
        is_squared = True
        with open(filename, "r") as f:
            for line in f:
                if "is_squared" in line:
                    if line.split()[-1] == "False":
                        is_squared = False
                    elif line.split()[-1] == "True":
                        is_squared = True
                    break
        return is_squared

    def _create_sf_label(self):
        freq_unit = self._variables["freq_unit"]
        if self._is_squared:
            superscript = "$^{\minus2}$"
        else:
            superscript = "$^{\minus1}$"
        sf_label = r"Spectral function ({}{})".format(freq_unit, superscript)
        return sf_label

    def create_total_sf(self):
        total_sf = []
        for i, data_point in enumerate(self._data_points):
            total_sf.append(data_point["total_sf"])
        return np.array(total_sf)

    def get_data_points(self):
        return self._data_points

    def set_data_points(self, data_points):
        self._data_points = data_points
