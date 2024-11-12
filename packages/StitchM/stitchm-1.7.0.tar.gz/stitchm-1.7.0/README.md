# StitchM
StitchM stitches together mosaic images taken in Cockpit (Micron)
into a universally readable format, currently '.ome.tiff'.

The current output is an 16bit greyscale image when stitching the mosaic.
Markers exported from Cockpit can be added as rectangular ROIs within the OME
metadata stored in the image header. ROIs can be imported and displayed using
bioformats in FIJI/ImageJ.

## Installation
Using pip: `python -m pip install StitchM`
Available on [PyPI](https://pypi.org/project/StitchM/) and [conda-forge](https://github.com/conda-forge/stitchm-feedstock). To use conda-forge, you may need to setup your conda by following instructions found [here](https://conda-forge.org/).

## Using StitchM:

- Command line script interface (accessible via `StitchM` or `stitchm`, use argument `--help` for more details)
- Drag and drop shortcut (created using `StitchM setup --windows-shortcut`) that processes mosaic .txt file and optional marker file if dragged on together, but cannot do batch processing of directories
- Module entry point (`python -m stitch_m`), which takes the paths of the mosaic and marker files in any order
- Imported package: `import stitch_m` or `from stitch_m import stitch_and_save, stitch, save`


## Motivation
To make a mosaic image that can be easily viewed and can be used for automatic 
alignment with a separate grid image (using gridSNAP).

## Features
- Creates OME-TIFF file from Cockpit's saved mosaic .txt file, which links to an .mrc file
  - OME metadata
  - Slight exposure trimming to remove extreme highlights
  - Image normalisation to fit data type
  - Optional filtering to remove fluorecence images (default can be changed in config file)
- Supports adding regions of interests (ROIs) to metadata using a .txt file containing markers, as can be saved from Cockpit
- Various default behaviours can be changed by editing a user config file (created using `StitchM setup --config`)

## Copyright

StitchM is licensed under a BSD license, please see LICENSE file.
Copyright (c) 2019-2021, Diamond Light Source Ltd. All rights reserved.

## Additional information

StitchM uses [OME metadata](https://docs.openmicroscopy.org/ome-model/latest/).

As Cockpit creates the images and accompanying files, so was referenced for the
creation of this software. Cockpit is licensed under GNU and can be found at
https://github.com/MicronOxford/cockpit
