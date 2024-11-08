# pyCFS-data

Data processing framework for openCFS (www.opencfs.org). This project contains Python libraries to easily create and
manipulate data stored in openCFS type HDF5 file format (`*.cfs`).

Documentation can be found in the [API Documentation](./generated/pyCFS.data.rst).

## Installation

Install via pip

```sh
pip install pycfs
```

Install with all dependencies for extras functionality.

```sh
pip install pycfs[data]
```

## [CFS IO](./generated/pyCFS.data.io.rst)

- [Reader class](./generated/pyCFS.data.io.CFSReader.rst) containing top and low-level methods for reading,
- [Writer class](./generated/pyCFS.data.io.CFSWriter.rst) containing top and low-level methods for writing,
- Data structure definitions for
    - [mesh](./generated/pyCFS.data.io.CFSMeshData.rst), containing description of the computational grid,
    - [result data](./generated/pyCFS.data.io.CFSResultData.rst), containing description of the result data,
    - [data array](./generated/pyCFS.data.io.CFSArray.rst), an overloaded numpy.ndarray.

### Example

```python
from pyCFS.data.io import CFSReader, CFSWriter

with CFSReader('file.cfs') as f:
    mesh = f.MeshData
    results = f.MultiStepData
with CFSWriter('file.cfs') as f:
    f.create_file(mesh_data=mesh, result_data=results)
```

## [Operators](./generated/pyCFS.data.operators.rst)

Utility functions for performing mesh and/or data manipulation

- [Transformation operators](./generated/pyCFS.data.operators.transformation.rst)
    - Fit geometry based on minimizing the squared source nodal distances to target nearest neighbor nodes.
- [Interpolators](./generated/pyCFS.data.operators.interpolators.rst): Node2Cell, Cell2Node, Nearest Neighbor (bidirectional), Projection-based linear interpolation

## [Extra functionality](./generated/pyCFS.data.extras.rst)

*Extras* provides Python libraries to easily manipulate data from various formats including

- [EnSight Case Gold](./generated/pyCFS.data.extras.ensight_io.rst) (`*.case`).
- [Ansys result file](./generated/pyCFS.data.extras.ansys_io.rst) (`*.rst`). Requires additional dependencies, which can be installed via pip

```sh
pip install pycfs[data]
```

- [PSV measurement data export file](./generated/pyCFS.data.extras.psv_io.rst) (`*.unv`).
- [MATLAB data files of NiHu structures and simulation results](./generated/pyCFS.data.extras.nihu_io.rst) (`*.mat`).

### EnSight Case Gold

- Utility functions for reading using *vtkEnSightGoldBinaryReader* and writing to *CFS HFD5*

### Ansys

- Utility functions for reading using *pyAnsys (ansys-dpf-core)* and writing to *CFS HFD5*
- Requires a licensed ANSYS DPF server installed on the system!
    - Check if the environment variable `ANSYSLMD_LICENSE_FILE` is set to the license server)!
    - Check if the environment variable `AWP_ROOTXXX` is set to the ANSYS installation root folder of the version you
      want to use (`vXXX` folder).

```sh
export ANSYSLMD_LICENSE_FILE=1055@my_license_server.ansys.com
export AWP_ROOTXXX=/usr/ansys_inc/vXXX
```

### PSV - Measurement data

- Utility functions for reading `*.unv` export files using *pyUFF* and writing to *CFS HFD5*
- Utility functions for manipulating data dictionary:
    - Interpolate data points from neighboring data points
    - Combine 3 measurements to 3D measurement

### NiHu

- Utility functions for reading `*.mat` MATLAB data files of NiHu structures and simulation results and writing to *CFS
  HFD5*

## Tutorial

Tutorial for using some of the main features of the pyCFS-data module. Download the whole script [here](examples/data_tutorial/data_tutorial.py).

1. Read file (download input file [here](examples/data_tutorial/tutorial_input.cfs))

```python
# %% Import CFS reader and writer classes
from pyCFS.data.io import CFSReader, CFSWriter

# %% Read mesh and result data of demo file
file_read = "tutorial_input.cfs"

with CFSReader(filename=file_read) as f:
    mesh = f.MeshData
    result_read = f.MultiStepData

# %% Print information about mesh and result
print(mesh)
print(result_read)
```

2. Apply time blending

```python
# %% Extract result
data_read = result_read.get_data_array(quantity="quantity", region="Vol")
# (optional) copy object to not edit the read structure
data_blended = data_read.copy()

# %% Apply simple time blending: Multiply with step value
for i in range(data_read.shape[0]):
    data_blended[i, :, :] *= data_blended.StepValues[i]
```

3. Add additional result steps

```python
# %% Extend result
import numpy as np
from pyCFS.data.io import CFSResultArray

# Extend step values array
step_values = np.append(data_blended.StepValues, data_blended.StepValues + 1.0)
# Extend data array
data_new = np.tile(np.ones(data_blended.shape[1:], dtype=complex), (5, 1, 1))
data_write = np.concatenate([data_blended, data_new], axis=0)
# Convert to CFSResultArray and reset MetaData
data_write = CFSResultArray(data_write)
data_write.MetaData = data_blended.MetaData
data_write.StepValues = step_values

# %% Create new result structure
from pyCFS.data.io import CFSResultData, cfs_types

result_write = CFSResultData(analysis_type=cfs_types.cfs_analysis_type.HARMONIC, data=[data_write])

```

4. Drop unused regions

```python
# %% Drop unused regions
regions_write = [mesh.get_region(region="Vol")]

mesh.drop_unused_nodes_elements(reg_data_list=regions_write)
```

5. Write file

```python
# %% Write mesh and result data to a new file
file_write = "tutorial_output.cfs"

with CFSWriter(filename=file_write) as f:
    f.create_file(mesh_data=mesh, result_data=result_write)
```