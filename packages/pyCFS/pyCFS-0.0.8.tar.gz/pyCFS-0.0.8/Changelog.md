# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- ( new features )

### Changed

- ( changes in existing functionality )

### Deprecated

- ( soon-to-be removed features )

### Removed

- ( now removed features )

### Fixed

- ( any bug fixes )
  
### Security

- ( in case of vulnerabilities )
  
## [0.0.8] - 2024-11-8

### Added

- ( new features )

### Changed

- ( changes in existing functionality )

### Deprecated

- ( soon-to-be removed features )

### Removed

- ( now removed features )

### Fixed

- ( any bug fixes )
- Removed linux dependent commands to python functions such that data management works independent of the underlying system
  
### Security

- ( in case of vulnerabilities )

## [0.0.7] - 2024-08-21

### Added

- ( new features )
- Extruding mesh to transformation operators
- Revolving mesh to transformation operators
- Read and Interpolate point result from Ansys RST file
- Nearest neighbor, cell to node, and node to cell interpolation utility functions
- Read PSV export data from 3D scan
- pyCFS.data.io object check before writing

### Changed

- ( changes in existing functionality )
- moved function `pyCFS.data.io.mesh_from_coordinates_connectivity`
to classmethod `pyCFS.data.io.CFSMeshData.from_coordinates_connectivity`

### Deprecated

- ( soon-to-be removed features )

### Removed

- ( now removed features )

### Fixed

- ( any bug fixes )
- Fixed ansys_io working with multiple Ansys Versions installed (currently working with Ansys 2022R2)
- Fixed reading of complex-valued history results
- Fixed Cell to Node / Node to Cell interpolation inconsistencies
- Fixed `AttributeError: pyCFS object has no attribute N` when invoking the `mesh_only` mode
  
### Security

- ( in case of vulnerabilities )

## [0.0.6] - 2024-05-08

### Added

- Compute surface normal vectors
- Option for parallel reading of result data (default now)

### Changed

- Vectorized element centroid computation
- Renamed "pyCFS.data.operators.fit_geometry" submodule to "pyCFS.data.operators.transformation"
- Renamed "pyCFS.data.operators.projection_interpolation.interpolation_fe" submodule to
  "pyCFS.data.operators.projection_interpolation.interpolation_matrix_projection_based"

## [0.0.5] - 2024-04-08

### Added

- Support for Reading/Writing MultiStepIDs other than 1.
- Support for Reading MultiStep with unsorted StepValues (requires sort before writing)

### Changed

- CFSResultData to contain data of a single MultiStep only.
- Improved testing using numpy.testing
- Improved import for better usability of data submodule
- Renamed nearest neighbor interpolator based on search direction

## [0.0.4] - 2024-03-25

### Added

- Possibility to read Meshes with groups/regions that have only Nodes defined. (As occuring when defining a nodeList)
  in an openCFS simulation.
- Method to find closest node/element for CFSMeshData objects
- Warning when element quality and centroids are not computed automatically due to size.

### Changed

- Website URL to openCFS Homepage.
- Testing of CFSReader to check read mesh and data values

### Fixed

- Critical bug when reading MultiStepData

## [0.0.3] - 2024-03-20

### Added

- Possibility to just run the meshing for the given parameters.
- Additional meshing setup control with `remeshing_on` and `mesh_present`
- `track_results` property to choose which results from the hdf file to track.
- Getter functions for hdf and sensor array results.

### Changed

- Running simulations in parallel does not do an initial mesh generation if `remeshing_on = False`.

### Removed

- `init_params` that needed to be passed to the `pyCFS` constructor, it is no longer used.

### Fixed

- Data module import.

## [0.0.2] - 2024-03-18

### Added

- `pyCFS.data` package
    - code, tests and doc
- Sensor array result support
    - Because CFS currently does not write SA results into the `hdf` file

### Changed

- Extended dependencies to accommodate `pyCFS.data` package

## [0.0.1] - 2024-03-12

### Added

- Old `pycfs` package code (refactored)
- CI pipeline for automated testing
- GitLab pages for documentation

### Fixed

- Parallelization when meshing
- Type hints

### Removed

- History results are no longer supported
    - These are now to be written into the `hdf` file
- Sensor array results are the only exception
    - When CFS can directly write these to the `hdf` file this package will change accordingly
    - Users should not see much difference in behavior