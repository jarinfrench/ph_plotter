#!/usr/bin/env python
import numpy as np


def read_band_yaml(yaml_file="band.yaml"):
    import yaml
    data = yaml.safe_load(open(yaml_file, "r"))
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
                    data['phonon'][iq]['band'][iband]['frequency'])
    return distance, frequency


def read_band_hdf5(hdf5_file="band.hdf5"):
    import h5py
    with h5py.File(hdf5_file, "r") as f:
        paths       = f["paths"]
        distances   = f["distances"]
        nqstars     = f["nqstars"]
        frequencies = f["frequencies"]
        pr_weights  = f["pr_weights"]

        paths       = np.array(paths)
        distances   = np.array(distances)
        nqstars     = np.array(nqstars)
        frequencies = np.array(frequencies)
        pr_weights  = np.array(pr_weights)

    return distances, frequencies, pr_weights, nqstars

def read_band_hdf5_dict(hdf5_file="band.hdf5"):
    import h5py
    data = {}
    with h5py.File(hdf5_file, "r") as f:
        for k, v in f.items():
            data[k] = np.array(v)
    return data
