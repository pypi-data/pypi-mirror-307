"""
Module containing data processing utilities for writing HDF5 files in openCFS format
"""

import copy
from copy import deepcopy

import h5py
import numpy as np
from pyCFS.data import io, v_def
from pyCFS.data.io.cfs_types import cfs_analysis_type, cfs_result_type
from .pycfs_data_fixtures import dummy_CFSMeshData_obj, dummy_CFSResultData_obj, dummy_CFSMeshData_linear_elements


def test_CFSMeshData(dummy_CFSMeshData_obj):

    print(dummy_CFSMeshData_obj.Quality)

    reg_info_demo = dummy_CFSMeshData_obj.Regions
    coord = dummy_CFSMeshData_obj.Coordinates
    conn = dummy_CFSMeshData_obj.Connectivity[1:, :]
    mesh_coord = io.CFSMeshData.from_coordinates_connectivity(coordinates=coord, connectivity=conn, element_dimension=2)
    print(mesh_coord)
    print(mesh_coord.Regions[0])


def test_CFSMeshData_element_centroids(dummy_CFSMeshData_obj):
    ref_sol = np.array([[0.5, 0.5, 0.5], [0.0, 1 / 3.0, 1 / 3.0], [0.0, 2 / 3.0, 2 / 3.0], [1.0, 0.5, 0.5]])
    np.testing.assert_array_equal(dummy_CFSMeshData_obj.ElementCentroids, ref_sol)

    ref_sol_reg = np.array([[0.5, 0.5, 0.5]])
    np.testing.assert_array_equal(dummy_CFSMeshData_obj.get_region_centroids(region="Vol"), ref_sol_reg)


def test_CFSMeshData_surface_normal(dummy_CFSMeshData_obj):
    ref_sol_el = np.array([[np.nan, np.nan, np.nan], [-1.0, 0, 0], [-1.0, 0, 0], [-1.0, 0, 0]])
    np.testing.assert_array_equal(dummy_CFSMeshData_obj.get_mesh_surface_normals(), ref_sol_el)

    ref_sol_node = np.tile(np.array([-1.0, 0, 0]), (8, 1))
    np.testing.assert_array_equal(
        dummy_CFSMeshData_obj.get_mesh_surface_normals(restype=cfs_result_type.NODE), ref_sol_node
    )


def test_CFSMeshData_from_various(dummy_CFSMeshData_linear_elements: io.CFSMeshData):
    coord = dummy_CFSMeshData_linear_elements.Coordinates
    conn = dummy_CFSMeshData_linear_elements.Connectivity
    el_types = dummy_CFSMeshData_linear_elements.Types
    regions = dummy_CFSMeshData_linear_elements.Regions

    merged_region = None
    for r in dummy_CFSMeshData_linear_elements.Regions:
        if merged_region is None:
            merged_region = r
        else:
            merged_region, _, _ = merged_region.merge(r)

    merged_region.Name = "region_all_entities"

    mesh_merged = copy.deepcopy(dummy_CFSMeshData_linear_elements)
    mesh_merged.Regions = [merged_region]
    mesh_merged.drop_unused_nodes_elements()

    mesh_data = io.CFSMeshData.from_coordinates_connectivity(
        coordinates=coord, connectivity=conn, element_types=el_types, region_name="region_all_entities"
    )

    assert mesh_data == mesh_merged

    for reg in dummy_CFSMeshData_linear_elements.Regions:

        coord = dummy_CFSMeshData_linear_elements.get_region_coordinates(reg)
        conn = dummy_CFSMeshData_linear_elements.get_region_connectivity(reg)

        mesh_single_reg = copy.deepcopy(dummy_CFSMeshData_linear_elements)
        mesh_single_reg.drop_unused_nodes_elements(reg_data_list=[reg])

        mesh_data = io.CFSMeshData.from_coordinates_connectivity(
            coordinates=coord, connectivity=conn, element_dimension=reg.Dimension, region_name=reg.Name
        )

        assert mesh_data == mesh_single_reg


def test_write(dummy_CFSMeshData_obj, dummy_CFSResultData_obj=None, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    print("Write demo file")
    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.create_file(mesh_data=dummy_CFSMeshData_obj, result_data=dummy_CFSResultData_obj)


def test_read_write_multistep2(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    test_write(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory)

    dummy_CFSResultData_obj2 = copy.deepcopy(dummy_CFSResultData_obj)
    dummy_CFSResultData_obj2.MultiStepID = 2
    dummy_CFSResultData_obj2.AnalysisType = cfs_analysis_type.HARMONIC

    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.write_multistep(result_data=dummy_CFSResultData_obj2, multi_step_id=2)

    with io.CFSReader(file, multistep_id=2, verbosity=v_def.all) as h5reader:
        np.testing.assert_equal(h5reader.MultiStepData, dummy_CFSResultData_obj2)


def test_read_mesh(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    test_write(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory)

    print("Read demo file")
    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        # Read Mesh
        print("Read Demo Mesh")
        mesh_data_read = h5reader.MeshData
        reg_info_read_S2 = h5reader.get_mesh_region(region="Surf2", is_group=True)
        reg_info_read = h5reader.MeshGroupsRegions

        # Check Read Mesh Data
        print("Check Written/Read Mesh")
        print(f" - Mesh Info: {dummy_CFSMeshData_obj.MeshInfo == mesh_data_read.MeshInfo}")
        print(f" - Mesh Data: {dummy_CFSMeshData_obj == mesh_data_read}")
        for reg_read in reg_info_read:
            print(f" - Region {reg_read.Name}: {reg_read in dummy_CFSMeshData_obj.Regions}")

        np.testing.assert_equal(dummy_CFSMeshData_obj, mesh_data_read)


def test_read_data(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    test_write(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory)

    print("Read demo file")
    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        # Read Mesh
        print("Read Demo Mesh")
        mesh_data_read = h5reader.MeshData

        # Read Data
        np.testing.assert_equal(h5reader.MultiStepData, dummy_CFSResultData_obj)

        node_id = h5reader.get_closest_node(coordinate=np.array([[0.1, 0, 0], [0, 0, 1]]), region="Vol")
        np.testing.assert_equal(
            mesh_data_read.get_closest_node(coordinate=np.array([[0.1, 0, 0], [0, 0, 1]]), region="Vol"), node_id
        )
        result_data_1 = [
            h5reader.get_single_data_steps(quantity="quantity", region="Vol", entity_id=node_id[i]) for i in node_id
        ]
        el_id = h5reader.get_closest_element(coordinate=np.array([[1, 1, 1], [0, 0, 0]]), region="Surf1")
        np.testing.assert_equal(
            mesh_data_read.get_closest_element(coordinate=np.array([[1, 1, 1], [0, 0, 0]]), region="Surf1"), el_id
        )
        result_data_1_3 = [
            h5reader.get_single_data_steps(quantity="quantity3", region="Surf1", entity_id=el_id[i]) for i in el_id
        ]


def test_read_data_sequential(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    test_write(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory)

    print("Read demo file")
    with io.CFSReader(file, processes=1, verbosity=v_def.all) as h5reader:
        # Read Mesh
        print("Read Demo Mesh")
        mesh_data_read = h5reader.MeshData

        # Read Data
        np.testing.assert_equal(h5reader.MultiStepData, dummy_CFSResultData_obj)


def test_read_group_wo_elements(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory="."):
    """Read group/region without elements (nodes only)."""

    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    test_write(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory)

    print("Delete Dataset /Mesh/Groups/")
    h5_path = f"Mesh/Regions/Surf1/Elements"
    with h5py.File(file, "r+") as f:
        del f[h5_path]

    with io.CFSReader(file, verbosity=v_def.all) as h5reader:
        mesh_data_read = h5reader.MeshData

    test_write(mesh_data_read, working_directory=working_directory)


def test_sort_result_data(dummy_CFSResultData_obj):
    # Write unsorted StepValues
    step_values = dummy_CFSResultData_obj.StepValues
    unsort_idx = np.arange(start=len(step_values) - 1, stop=-1, step=-1)
    step_values = step_values[unsort_idx]
    dummy_CFSResultData_obj.StepValues = step_values

    # Sort ResultData by StepValues
    sort_idx = dummy_CFSResultData_obj.sort_steps(return_idx=True)
    np.testing.assert_array_equal(sort_idx, unsort_idx)


def test_reorient(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    dummy_CFSMeshData_obj.reorient_region("Surf1")
    dummy_CFSMeshData_obj.reorient_region("Surf2")
    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.create_file(mesh_data=dummy_CFSMeshData_obj, result_data=dummy_CFSResultData_obj)


def test_manipulate_result_data(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    result_data_extract = dummy_CFSResultData_obj.extract_quantity_region("quantity3", "Surf1")
    result_data_other = dummy_CFSResultData_obj.extract_quantity_region("quantity", "Vol")
    result_data_other_selection = result_data_other[[0, 2]]
    result_data_write = result_data_other.combine_with(result_data_extract)[1:3]
    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.create_file(mesh_data=dummy_CFSMeshData_obj, result_data=result_data_write)


def test_remove_region(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    print("Remove region and write reduced mesh and data")
    reg_info_keep = [dummy_CFSMeshData_obj.Regions[i] for i in [1, 2]]
    node_idx, elem_idx = reg_info_keep[0].update_nodes_from_connectivity(
        elems=np.array([2]), connectivity=dummy_CFSMeshData_obj.Connectivity
    )
    dummy_CFSMeshData_obj.drop_unused_nodes_elements(reg_data_list=reg_info_keep)
    result_data_extract = dummy_CFSResultData_obj.extract_quantity_region("quantity3", "Surf1", data_ids=elem_idx)
    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.create_file(mesh_data=dummy_CFSMeshData_obj, result_data=result_data_extract)


def test_merge_meshes(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    print("Merge meshes")
    mesh_data_1 = deepcopy(dummy_CFSMeshData_obj)
    mesh_data_2 = deepcopy(dummy_CFSMeshData_obj)

    mesh_data_2.convert_quad2tria(idx_convert=np.array([3]))

    reg_info_1 = [mesh_data_1.Regions[i] for i in [0]]
    reg_info_2 = [mesh_data_2.Regions[i] for i in [2]]

    mesh_data_1.drop_unused_nodes_elements(reg_data_list=reg_info_1)
    mesh_data_2.drop_unused_nodes_elements(reg_data_list=reg_info_2)

    mesh_merged = mesh_data_1.merge(mesh_data_2)
    mesh_added = mesh_data_1 + mesh_data_2
    print(mesh_merged == mesh_added)

    with io.CFSWriter(file, verbosity=v_def.all) as h5writer:
        h5writer.create_file(mesh_data=mesh_merged)


def test_convert_to_simplex(dummy_CFSMeshData_obj, dummy_CFSResultData_obj, working_directory="."):
    file = f"{working_directory}/tests/data_tmp/pycfs_data_io.cfs"

    dummy_CFSMeshData_obj.update_mesh_centroids()

    result = dummy_CFSMeshData_obj.convert_to_simplex(result_data=dummy_CFSResultData_obj)
    dummy_CFSMeshData_obj.update_mesh_quality()

    with io.CFSWriter(file, verbosity=v_def.all) as f:
        f.create_file(dummy_CFSMeshData_obj, result)
