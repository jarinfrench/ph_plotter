#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import sys

sys.path.append("../ph_plotter")
from ph_plotter.common_arguments_adder import CommonArgumentsAdder

__author__ = "Yuji Ikeda"


def run(variables):
    sf_with = variables.pop("sf_with")

    if sf_with == "e1":
        from ph_plotter.points_sf_e1_plotter import PointsSFE1Plotter as PointsSFPlotter

    elif sf_with == "e2":
        from ph_plotter.points_sf_e2_plotter import PointsSFE2Plotter as PointsSFPlotter

    elif sf_with == "irs":
        from ph_plotter.points_sf_irs_plotter import (
            PointsSFIRsPlotter as PointsSFPlotter,
        )

    elif sf_with == "atoms":
        from ph_plotter.points_sf_atoms_plotter import (
            PointsSFAtomsPlotter as PointsSFPlotter,
        )

    PointsSFPlotter(variables).run()


def main():
    import argparse

    parser = argparse.ArgumentParser()
    CommonArgumentsAdder().add_common_arguments(parser)
    parser.add_argument(
        "--data_file", default="sf.hdf5", type=str, help="Filename of data."
    )
    parser.add_argument(
        "--sf_with",
        type=str,
        choices=["e1", "e2", "irs", "atoms"],
        required=True,
        help="To be plotted with the total spectral functions.",
    )
    parser.add_argument(
        "--selected_irreps",
        type=json.loads,
        help="Specification of Small Reps. ex. {'mm2': ['B2']}",
    )
    parser.add_argument("--points", nargs="+", type=int, help="Points to be plotted")
    parser.add_argument(
        "--fill",
        dest="is_filled",
        action="store_true",
        help="Partial SFs are filled by color.",
    )
    args = parser.parse_args()

    print(vars(args))
    run(vars(args))


if __name__ == "__main__":
    main()
