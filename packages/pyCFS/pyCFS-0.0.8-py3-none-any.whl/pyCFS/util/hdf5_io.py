import h5py
import numpy as np
from typing import List, Optional, Tuple
from .lib_types import nestedResultDict


# Constants :
RESULT_DESCRIPTION: str = "ResultDescription"
RESULTS: str = "Results"
MESH: str = "Mesh"
NODES: str = "Nodes"
ELEMENTS: str = "Elements"
REAL: str = "Real"
IMAG: str = "Imag"
MULTISTEP: str = "MultiStep_"
DATA: str = "data"
HISTORY: str = "History"
ALL: str = "all"


def get_result_names(file_path: str) -> List[str]:
    """Returns a list containing the names of the results which are given in the
    hdf file located at the file_path.

    Args:
        file_path (str): path to the hdf5 file.

    Returns:
        List[str]: list of result names.
    """

    hdf5_file = h5py.File(file_path, "r")
    return list(hdf5_file[RESULTS][MESH][f"{MULTISTEP}1"][RESULT_DESCRIPTION])


def get_history_results(hdf5_file: h5py.File, dtype: type = np.float64) -> nestedResultDict:
    # TODO : make check if history results empty to return empty dict!
    results: nestedResultDict = {}
    dict_empty = True

    a = b = np.array([])

    if HISTORY in list(hdf5_file[RESULTS].keys()):
        dict_empty = False
        multisteps_list = list(hdf5_file[RESULTS][HISTORY].keys())

        for multistep in multisteps_list:
            results_list = list(hdf5_file[RESULTS][HISTORY][multistep].keys())
            results_list.remove(RESULT_DESCRIPTION)

            results[multistep] = {}
            for result in results_list:
                result_groups = list(hdf5_file[RESULTS][HISTORY][multistep][result].keys())

                results[multistep][result] = {}
                for result_group in result_groups:
                    group_elements = list(hdf5_file[RESULTS][HISTORY][multistep][result][result_group].keys())

                    results[multistep][result][result_group] = {}
                    for group_element in group_elements:
                        data_types = list(
                            hdf5_file[RESULTS][HISTORY][multistep][result][result_group][group_element].keys()
                        )

                        results[multistep][result][result_group][group_element] = {}

                        if REAL in data_types:
                            a = np.array(
                                hdf5_file[RESULTS][HISTORY][multistep][result][result_group][group_element][REAL],
                                dtype=dtype,
                            )
                        if IMAG in data_types:
                            b = 1j * np.array(
                                hdf5_file[RESULTS][HISTORY][multistep][result][result_group][group_element][IMAG],
                                dtype=dtype,
                            )

                        results[multistep][result][result_group][group_element][DATA] = (
                            a + b if IMAG in data_types else a
                        )

    if dict_empty:
        results = {}

    return results


def get_results(
    file_path: str, result_names: Optional[str | List[str]] = None, dtype: type = np.float64
) -> Tuple[nestedResultDict, nestedResultDict]:
    """Reads the hdf5 file located at file_path and extracts the results given
    in the result_names list. If this list is None then all of the results are read.

    Args:
        file_path (str): path to the hdf5 file.
        result_names (Optional[List[str]], optional): list of result names which we want to extract. Defaults to None.

    Returns:
        nestedResultDict: nested dictionary containing the results.
    """
    results: nestedResultDict = {}

    dict_empty = True
    hdf5_file = h5py.File(file_path, "r")

    multisteps_list = list(hdf5_file[RESULTS][MESH].keys())

    for multistep in multisteps_list:

        steps_list = list(hdf5_file[RESULTS][MESH][multistep].keys())

        steps_list.remove(RESULT_DESCRIPTION)

        results[multistep] = {}
        for step in steps_list:
            result_list = list(hdf5_file[RESULTS][MESH][multistep][step].keys())

            results[multistep][step] = {}
            for result in result_list:

                should_fetch = (type(result_names) is str) and (result_names is ALL)
                if not should_fetch and type(result_names) is list:
                    should_fetch = result in result_names

                if should_fetch:
                    dict_empty = False
                    region_list = list(hdf5_file[RESULTS][MESH][multistep][step][result].keys())

                    results[multistep][step][result] = {}
                    for region in region_list:

                        results[multistep][step][result][region] = {}
                        res_types = list(hdf5_file[RESULTS][MESH][multistep][step][result][region].keys())

                        if NODES in res_types:

                            data_types = list(hdf5_file[RESULTS][MESH][multistep][step][result][region][NODES].keys())
                            if REAL in data_types:
                                results[multistep][step][result][region][DATA] = np.array(
                                    hdf5_file[RESULTS][MESH][multistep][step][result][region][NODES][REAL],
                                    dtype=dtype,
                                )
                            if IMAG in data_types:
                                results[multistep][step][result][region][DATA] += 1j * (
                                    np.array(
                                        hdf5_file[RESULTS][MESH][multistep][step][result][region][NODES][IMAG],
                                        dtype=dtype,
                                    )
                                )

                        else:

                            data_types = list(
                                hdf5_file[RESULTS][MESH][multistep][step][result][region][ELEMENTS].keys()
                            )
                            if REAL in data_types:
                                results[multistep][step][result][region][DATA] = np.array(
                                    hdf5_file[RESULTS][MESH][multistep][step][result][region][ELEMENTS][REAL],
                                    dtype=dtype,
                                )
                            if IMAG in data_types:
                                results[multistep][step][result][region][DATA] += 1j * (
                                    np.array(
                                        hdf5_file[RESULTS][MESH][multistep][step][result][region][ELEMENTS][IMAG],
                                        dtype=dtype,
                                    )
                                )

    history_results = get_history_results(hdf5_file, dtype=dtype)
    if dict_empty:
        results = {}

    return results, history_results
