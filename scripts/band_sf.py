#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

__author__ = "Yuji Ikeda"

import json
import numpy as np
from ph_plotter.common_arguments_adder import CommonArgumentsAdder


def run(variables):
    plot_style = variables.pop("plot_style")

    if plot_style == "mesh":
        from ph_plotter.band_sf_mesh_plotter import (
            BandSFMeshPlotter as BandSFPlotter)

    elif plot_style == "contour":
        from ph_plotter.band_sf_contour_plotter import (
            BandSFContourPlotter as BandSFPlotter)

    elif plot_style == "imshow":
        from ph_plotter.band_sf_imshow_plotter import (
            BandSFImshowPlotter as BandSFPlotter)

    BandSFPlotter(variables).run()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    CommonArgumentsAdder().add_common_arguments(parser)
    parser.add_argument("--data_file",
                        default="sf.hdf5",
                        type=str,
                        help="Filename of data.")
    parser.add_argument("--sf_with",
                        type=str,
                        choices=["elements", "irreps"],
                        required=True,
                        help="To be plotted with total spectral functions.")
    parser.add_argument("--plot_style",
                        type=str,
                        choices=["mesh", "contour", "imshow"],
                        required=True,
                        help="Plot style for spectral fucntions.")
    parser.add_argument("--ninterp",
                        type=int,
                        help="Interpolation number.")
    parser.add_argument("--selected_irreps",
                        type=json.loads,
                        help="Specification of Small Reps. ex. {'mm2': ['B2']}")
    parser.add_argument("--combinations_elements",
                        nargs='+',
                        type=str,
                        help="Specification of Combinations of elements. ex. Cu Cu Au Au")
    args = parser.parse_args()

    if args.combinations_elements is not None:
        args.combinations_elements = np.array(args.combinations_elements).reshape(-1, 2)

    print(vars(args))
    run(vars(args))


if __name__ == "__main__":
    main()
