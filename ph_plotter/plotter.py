#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os

import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler

__author__ = "Yuji Ikeda"


def use_classic_ticks():
    # For back-compatibility to matplotlib.1.5.3
    params = {
        "xtick.top": True,
        "xtick.direction": "in",
        "ytick.right": True,
        "ytick.direction": "in",
    }
    plt.rcParams.update(params)


def update_prop_cycle(linewidth):
    # https://github.com/vega/vega/wiki/Scales#scale-range-literals
    colors = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ] * 3
    dashes_list = [
        (4, 1),
        (2, 1),
        (4, 1, 2, 1),
        (4, 1, 2, 1, 2, 1),
        (4, 1, 2, 1, 2, 1, 2, 1),
        (8, 1, 4, 1),
    ] * 5
    for i, dashes in enumerate(dashes_list):
        dashes_list[i] = _modify_dashes_by_linewidth(dashes, linewidth)

    plt.rc("axes", prop_cycle=cycler("color", colors) + cycler("dashes", dashes_list))


def _modify_dashes_by_linewidth(dashes, linewidth):
    return tuple(np.array(dashes) * linewidth)


def read_primitive_matrix(phonopy_conf):
    from phonopy.cui.settings import fracval

    with open(phonopy_conf) as f:
        for line in f.readlines():
            if "PRIMITIVE_AXIS" in line:
                tmp = [fracval(s) for s in line.split("=")[-1].split()]
                return np.array(tmp).reshape(3, 3)
    return np.eye(3)


def read_band_labels(phonopy_conf):
    return BandLabelReader().read(phonopy_conf)


class BandLabelReader:
    def read(self, phonopy_conf):
        import yaml

        try:
            yaml_file = "band.yaml"
            data = yaml.safe_load(open(yaml_file, "r"))
            tmp = data["labels"]
            band_labels = []
            l1_old = ""
            for i, (l0, l1) in enumerate(tmp):
                if i == 0:
                    band_labels.append(l0)
                elif l0 == l1_old:
                    band_labels.append(l0)
                else:
                    band_labels.append("{}|{}".format(l1_old, l0))
                l1_old = l1
            band_labels.append(l1)
            return band_labels
        except:
            return self.read_from_conf(phonopy_conf)

    def read_from_conf(self, phonopy_conf):
        band_labels = None
        with open(phonopy_conf) as f:
            for line in f.readlines():
                if "BAND_LABELS" in line:
                    band_labels = line.split("=")[-1].split()

        gamma_str = r"\Gamma"
        if band_labels is not None:
            for i, band_label in enumerate(band_labels):
                band_labels[i] = band_label.replace(gamma_str, "Γ")
            band_labels = tuple(band_labels)
        return band_labels


class Plotter(object):
    def __init__(self, variables=None, is_horizontal=False):
        if variables is None:
            variables = {}
        self._create_default_variables()
        self.update_variables(variables)

        self._is_horizontal = is_horizontal

    def _create_default_variables(self):
        self._variables = {
            "freq_unit": "THz",
            "unit": 1.0,
            "f_min": -2.0,
            "f_max": 10.0,
            "d_freq": 2.0,
            "dos_min": 0.0,
            "dos_max": 0.4,
            "dos_ticks": 0.1,
            "sf_min": 0.0,
            "sf_max": 2.0,
            "d_sf": 0.5,
            "figure_type": "pdf",
            "figsize": (5.0, 3.5),
            "fontsize": 12.0,
            "linecolor": "k",
            "linewidth": 1,
            "dashes": (),
            "colormap_p": "r",
            "colormap_n": "w",
            "alpha": 1.0,
            "is_transparent_gradient": False,
            "markersize": 5.0,
            "poscar": "POSCAR",
            "sf_with": "atoms",
            "ninterp": None,
            "selected_irreps": None,
            "combinations_elements": None,
            "elements": None,
            "points": None,
            "is_filled": False,
            "dir": ".",
        }

    def update_variables(self, variables):
        for k, v in variables.items():
            if v is not None:
                # if k in ["colormap_p", "colormap_n"]:
                #     self._variables[k] = v.replace("[", "").replace("]", "").split(".")
                self._variables[k] = v

    def update_rcParams(self):
        variables = self._variables

        # fontsize = variables['fontsize']
        # params = {
        #     "font.family": "Arial",
        #     "font.size": fontsize,
        #     # "mathtext.fontset": "custom",
        #     # "mathtext.it": "Arial",
        #     "mathtext.default": "regular",
        #     "legend.fontsize": fontsize,
        # }
        # plt.rcParams.update(params)
        use_classic_ticks()
        update_prop_cycle(
            variables["linewidth"]
        )  # This may be not needed for matplotlib 2.x

    def load_data(self):
        raise NotImplementedError

    def configure(self, ax):
        raise NotImplementedError

    def plot(self, ax):
        raise NotImplementedError

    def create_figure_name(self):
        raise NotImplementedError

    def prepare_figure(self, fig, ax):
        self.update_rcParams()
        if fig is None or ax is None:
            fig, ax = plt.subplots(
                1,
                1,
                figsize=self._variables["figsize"],
                frameon=False,
                tight_layout=True,
            )
        else:
            fig.set_size_inches(self._variables["figsize"])
            fig.set_frameon(False)
            fig.tight_layout()
            ax.set_position([0.1, 0.1, 0.8, 0.8])
        return fig, ax

    def close(self):
        plt.close()

    def create_figure(self, fig, ax, close=True):
        fig, ax = self.prepare_figure(fig, ax)
        figure_name = self.create_figure_name()

        self.configure(ax)
        self.plot(ax)
        self.save_figure(fig, figure_name)

        if close:
            self.close()

    def save_figure(self, fig, figure_name):
        fig.savefig(figure_name, transparent=True)

    def run(self, fig=None, ax=None, close=True):
        variables = self._variables

        self.load_data("/".join([variables["dir"], variables["data_file"]]))

        variables.update(
            {
                "freq_unit": "THz",
                "unit": 1.0,
            }
        )
        self.update_variables(variables)
        self.create_figure(fig, ax, close)

        return

        from scipy.constants import Planck, eV

        THz2meV = Planck / eV * 1e15  # 4.135667662340164

        # meV
        variables.update(
            {
                "freq_unit": "meV",
                "unit": THz2meV,
            }
        )
        scale = 4.0
        variables["f_min"] *= scale
        variables["f_max"] *= scale
        variables["d_freq"] *= scale
        self.update_variables(variables)
        self.create_figure()

    def create_primitive(self, filename="POSCAR", conf_file=None):
        from phonopy.interface.vasp import read_vasp
        from phonopy.structure.cells import get_primitive

        if conf_file is None:
            self._check_conf_files()
        else:
            self.set_conf_file(conf_file)
        primitive_matrix = self._read_primitive_matrix()
        atoms = read_vasp(filename)
        return get_primitive(atoms, primitive_matrix)

    def _read_primitive_matrix(self):
        return read_primitive_matrix(self._conf_file)

    def _check_conf_files(self):
        conf_files = [
            "band.conf",
            "dos_smearing.conf",
            "dos_tetrahedron.conf",
            "partial_dos_smearing.conf",
            "partial_dos_tetrahedron.conf",
        ]
        for conf_file in conf_files:
            if os.path.isfile(conf_file):
                self.set_conf_file(conf_file)
                return

    def set_conf_file(self, conf_file):
        self._conf_file = conf_file

    def get_object_plotted(self):
        return self._object_plotted
