import sys
from itertools import product

import matplotlib.pyplot as plt
import numpy as np

sys.path.append("/home/frenjc/HECC/2.HECC/ph_plotter")

dirs = [
    "6.Binary_alloy/6.Ta_0.5_Nb_0.5_C/2.PD/1.upho",
    "6.Binary_alloy/7.Zr_0.5_Ti_0.5C/2.PD/1.upho",
    "6.Binary_alloy/8.Zr_0.5_Ta_0.5_C/2.PD/1.upho",
    "6.Binary_alloy/9.Zr0.5Nb0.5C/2.phpy/1.upho",
    "6.Binary_alloy/11.Zr_0.5_Hf_0.5_C/2.PD/1.upho",
    "7.Ternary_alloy/1.Zr_Ti_Ta_C/2.phpy/1.upho",
    "7.Ternary_alloy/2.Zr_Ti_Hf_C/3.PhPy/1.upho",
    "7.Ternary_alloy/3.Zr_Ti_Nb_C/3.phpy/1.upho",
    "7.Ternary_alloy/4.Zr_Hf_Nb_C/3.phpy/1.upho",
    "8.quadnary_alloy/1.Zr_Ti_Ta_Nb_C/3.Phpy/upho",
    "8.quadnary_alloy/2.Zr_Ti_Ta_Hf/3.phpy/1.upho",
    "9.5HECC/2.SQS/1.216_atoms/1.ZrNbHfTiTaC/2.Geo/3.phpy/1.upho",
]
elements = {
    dirs[0]: [None, "Ta", "Nb", "C"],
    dirs[1]: [None, "Zr", "Ti", "C"],
    dirs[2]: [None, "Zr", "Ta", "C"],
    dirs[3]: [None, "Zr", "Nb", "C"],
    dirs[4]: [None, "Zr", "Hf", "C"],
    dirs[5]: [None, "Zr", "Ti", "Ta", "C"],
    dirs[6]: [None, "Zr", "Ti", "Hf", "C"],
    dirs[7]: [None, "Zr", "Ti", "Nb", "C"],
    dirs[8]: [None, "Zr", "Hf", "Nb", "C"],
    dirs[9]: [None, "Zr", "Ti", "Ta", "Nb", "C"],
    dirs[10]: [None, "Zr", "Ti", "Ta", "Hf", "C"],
    dirs[11]: [None, "Zr", "Ti", "Ta", "Hf", "Nb", "C"],
}
combinations = {i: list(product(elements[i][1:], elements[i][1:])) for i in dirs}

for di in dirs:
    for el in elements[di]:
        # Required arguments. Defaults are provided
        combinations_elements = None
        variables = dict(
            alpha=1,
            colormap_n=["w"],
            colormap_p=[
                "lightgreen",
                "green",
                "yellowgreen",
                "yellow",
                "orange",
                "darkorange",
                "orangered",
                "red",
            ],
            combinations_elements=np.array(combinations_elements).reshape(-1, 2)
            if combinations_elements is not None
            else None,
            d_freq=5.0,
            d_sf=0.2,
            dashes=[],
            data_file="sf.hdf5",
            dir=di,
            dos_max=0.4,
            elements=[el] if el is not None else None,
            f_max=25.0,
            f_min=0.0,
            figsize=(5.0, 3.5),
            figure_type="pdf",
            fontsize=None,
            linecolor=None,
            linewidth=1.0,
            ninterp=None,
            poscar="POSCAR",
            selected_irreps=None,
            sf_max=1.0,
            sf_min=0.0,
        )
        plot_style = "mesh"  # Choose from "mesh", "contour", and "imshow"

        if plot_style == "mesh":
            from ph_plotter.band_sf_mesh_plotter import (
                BandSFMeshPlotter as BandSFPlotter,
            )
        elif plot_style == "contour":
            from ph_plotter.band_sf_contour_plotter import (
                BandSFContourPlotter as BandSFPlotter,
            )
        elif plot_style == "imshow":
            from ph_plotter.band_sf_imshow_plotter import (
                BandSFImshowPlotter as BandSFPlotter,
            )
        bsfp = BandSFPlotter(variables)
        plt.close("all")
        plt.rcParams.update(plt.rcParamsDefault)
        fig, ax = plt.subplots()
        print(variables)
        bsfp.run(fig, ax, close=False)
        scale = 1.0
        data = []
        band_length = 0
        num_bands = 0
        with open(
            "/".join(
                [variables["dir"], "3.weight_FC/average_mass_FC_band_structure.txt"]
            ),
            "r",
        ) as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    if "End points of segments" in line:
                        continue
                    else:
                        scale = 1 / float(line[1:].split()[-1])
                elif not line:
                    continue
                else:
                    d = [float(i) for i in line.split()]
                    if d[0] == 0:
                        band_length = 0
                        num_bands += 1
                    band_length += 1
                    data.append([scale * d[0], d[1]])
        data = np.array(data)

        for i in range(num_bands):
            ax.plot(
                data[i * band_length : (i + 1) * band_length, 0],
                data[i * band_length : (i + 1) * band_length, 1],
                "k",
                linestyle="-",
                lw=1.5,
            )

        plt.savefig(
            "/".join(
                [
                    variables["dir"],
                    f'band_sf_THz_{f"{el}" if el is not None else "".join(elements[di][1:])}.pdf',
                ]
            )
        )
        plt.close()

    for combo in combinations[di]:
        variables = dict(
            alpha=1,
            colormap_n=["w"],
            colormap_p=[
                "lightgreen",
                "green",
                "yellowgreen",
                "yellow",
                "orange",
                "darkorange",
                "orangered",
                "red",
            ],
            combinations_elements=np.array(combo).reshape(-1, 2)
            if combo is not None
            else None,
            d_freq=5.0,
            d_sf=0.2,
            dashes=[],
            data_file="sf.hdf5",
            dir=di,
            dos_max=0.4,
            elements=None,
            f_max=25.0,
            f_min=0.0,
            figsize=(5.0, 3.5),
            figure_type="pdf",
            fontsize=None,
            linecolor=None,
            linewidth=1.0,
            ninterp=None,
            poscar="POSCAR",
            selected_irreps=None,
            sf_max=1.0,
            sf_min=0.0,
        )
        plot_style = "mesh"  # Choose from "mesh", "contour", and "imshow"

        if plot_style == "mesh":
            from ph_plotter.band_sf_mesh_plotter import (
                BandSFMeshPlotter as BandSFPlotter,
            )
        elif plot_style == "contour":
            from ph_plotter.band_sf_contour_plotter import (
                BandSFContourPlotter as BandSFPlotter,
            )
        elif plot_style == "imshow":
            from ph_plotter.band_sf_imshow_plotter import (
                BandSFImshowPlotter as BandSFPlotter,
            )
        bsfp = BandSFPlotter(variables)
        plt.close("all")
        plt.rcParams.update(plt.rcParamsDefault)
        fig, ax = plt.subplots()
        print(variables)
        bsfp.run(fig, ax, close=False)
        scale = 1.0
        data = []
        band_length = 0
        num_bands = 0
        with open(
            "/".join(
                [variables["dir"], "3.weight_FC/average_mass_FC_band_structure.txt"]
            ),
            "r",
        ) as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    if "End points of segments" in line:
                        continue
                    else:
                        scale = 1 / float(line[1:].split()[-1])
                elif not line:
                    continue
                else:
                    d = [float(i) for i in line.split()]
                    if d[0] == 0:
                        band_length = 0
                        num_bands += 1
                    band_length += 1
                    data.append([scale * d[0], d[1]])
        data = np.array(data)

        for i in range(num_bands):
            ax.plot(
                data[i * band_length : (i + 1) * band_length, 0],
                data[i * band_length : (i + 1) * band_length, 1],
                "k",
                linestyle="-",
                lw=1.5,
            )

        plt.savefig(
            "/".join([variables["dir"], f"band_sf_THz_{combo[0]}{combo[1]}.pdf"])
        )
        plt.close()
