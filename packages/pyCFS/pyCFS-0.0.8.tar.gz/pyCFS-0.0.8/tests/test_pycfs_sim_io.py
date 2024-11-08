from pyCFS import pyCFS
from pyCFS.util.hdf5_io import get_history_results
from .pycfs_fixtures import sensor_array_result_file, hdf_result_file_real, hdf_result_file_imag
import numpy as np
import os
import h5py


def test_read_sa_result(sensor_array_result_file):
    sa_result = pyCFS._read_sa_result(sensor_array_result_file["file"])
    assert sa_result["columns"] == sensor_array_result_file["columns"]
    assert np.all(sa_result["data"] == sensor_array_result_file["data"])


def test_split_sa_result_name(sensor_array_result_file):
    name_split = pyCFS._split_sa_result_name(sensor_array_result_file["file"], "")
    assert name_split == sensor_array_result_file["file_split"]


def test_is_coord_col():
    assert pyCFS._is_coord_col("origElemNum") == True
    assert pyCFS._is_coord_col("globCoord-x") == True
    assert pyCFS._is_coord_col("globCoord-y") == True
    assert pyCFS._is_coord_col("globCoord-z") == True
    assert pyCFS._is_coord_col("locCoord-xi") == True
    assert pyCFS._is_coord_col("locCoord-eta") == True
    assert pyCFS._is_coord_col("locCoord-zeta") == True
    assert pyCFS._is_coord_col("elecFieldIntensity-z") == False
    assert pyCFS._is_coord_col("elecPotential") == False


def test_remove_coord_cols(sensor_array_result_file):
    sa_result = pyCFS._read_sa_result(sensor_array_result_file["file"])
    sa_result_no_coord = pyCFS._remove_coord_cols(sa_result)

    assert sa_result["columns"] == sensor_array_result_file["columns"]
    assert np.all(sa_result["data"] == sensor_array_result_file["data"])
    assert sa_result_no_coord["columns"] == sensor_array_result_file["columns_nocoord"]
    assert np.all(sa_result_no_coord["data"] == sensor_array_result_file["data_nocoord"])


def test_write_read_contents():
    contents = "secret test message"
    file = "./tests/data/sim_io/temp_file.txt"

    pyCFS.write_file_contents(file, contents)
    read_contents = pyCFS.read_file_contents(file)

    assert read_contents == contents


def test_find_and_remove_files():
    wildcards = ["./tests/data/sim_io/*file.txt"]
    pyCFS._find_and_remove_files(wildcards)

    assert os.path.exists("./tests/data/sim_io/temp_file.txt") == False


def test_hdf5_io_get_history_results_real(hdf_result_file_real):

    results = get_history_results(hdf_result_file_real["hdf5_file"])

    assert np.allclose(hdf_result_file_real["result"], 
                       results["MultiStep_3"]["mechDisplacement"]["Nodes"]["406"]["data"])

def test_hdf5_io_get_history_results_imag(hdf_result_file_imag):
   
    results = get_history_results(hdf_result_file_imag["hdf5_file"])

    assert np.allclose(hdf_result_file_imag["result"], 
                       results["MultiStep_1"]["waterSurfaceForce"]["ElementGroup"]["S_glass-water"]["data"])
