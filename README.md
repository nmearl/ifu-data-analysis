# IFU Data Analysis

Project home for a new breed of quick IFU data analysis tools.

## Attribution
Efforts for this project is being done at the Space Telescope Science Institute. All work is tentatively released under a 3-clause BSD license. See LICENSE for more details.
 
## Modules
The package will be broken into modules, each with a distinct set of functionality.

- *Arithmetic*:
 - Basic math operations on multi-dimensional data.
 - Collapsing data-cubes into 2D images
 - Extracting 1D spectral traces
 - Continuum subtraction
 - Emission line ratios from multiple transitions
- *Analysis*:
 - Kinematics from multiple gas components (via Gaussian fitting).
 - Kinematics from stellar continuum emission (via 1D template fitting).
- *Manipulation*:
 - Spatial resolution matching (cube-matching to common resolutions)
 - Multi-datacube interaction (cubes with difference sampling sensitivities, or from different instruments).
- *Presentation*:
 - Publication quality velocity channel maps,
 - Colored velocity/moment maps,
 - Position-velocity maps, and more.
