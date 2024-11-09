# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['concatenator', 'concatenator.harmony']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=8.4.0',
 'netcdf4>=1.6.5',
 'pystac>=0.5.3',
 'xarray>=2024.3.0']

entry_points = \
{'console_scripts': ['stitchee = concatenator.run_stitchee:main',
                     'stitchee_harmony = concatenator.harmony.cli:main']}

setup_kwargs = {
    'name': 'stitchee',
    'version': '1.5.0',
    'description': 'NetCDF4 Along-existing-dimension Concatenation Service',
    'long_description': '<p align="center">\n    <img alt="stitchee, a python package for concatenating netCDF data along an existing dimension"\n    src="https://github.com/danielfromearth/stitchee/assets/114174502/58052dfa-b6e1-49e5-96e5-4cb1e8d14c32" width="250"\n    />\n</p>\n\n<p align="center">\n    <a href="https://www.repostatus.org/#active" target="_blank">\n        <img src="https://www.repostatus.org/badges/latest/active.svg" alt="Project Status: Active – The project has reached a stable, usable state and is being actively developed">\n    </a>\n    <a href=\'https://stitchee.readthedocs.io/en/latest/?badge=latest\'>\n        <img src=\'https://readthedocs.org/projects/stitchee/badge/?version=latest\' alt=\'Documentation Status\' />\n    </a>\n    <a href="https://github.com/python/black" target="_blank">\n        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style">\n    </a>\n    <a href="http://mypy-lang.org/" target="_blank">\n        <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Mypy checked">\n    </a>\n    <a href="https://pypi.org/project/stitchee/" target="_blank">\n        <img src="https://img.shields.io/pypi/pyversions/stitchee.svg" alt="Python Versions">\n    </a>\n    <a href="https://pypi.org/project/stitchee" target="_blank">\n        <img src="https://img.shields.io/pypi/v/stitchee?color=%2334D058label=pypi%20package" alt="Package version">\n    </a>\n    <a href="https://codecov.io/gh/nasa/stitchee">\n     <img src="https://codecov.io/gh/nasa/stitchee/graph/badge.svg?token=WDj92iN7c4" alt="Code coverage">\n    </a>\n</p>\n\n[//]: # (Using deprecated `align="center"` for the logo image and badges above, because of https://stackoverflow.com/a/62383408)\n\n# Overview\n_____\n\n_STITCHEE_ (STITCH by Extending a dimEnsion) is used for concatenating netCDF data *along an existing dimension*,\nand it is designed as both a standalone utility and for use as a service in [Harmony](https://harmony.earthdata.nasa.gov/).\n\n## Getting started, with poetry\n\n1. Follow the instructions for installing `poetry` [here](https://python-poetry.org/docs/).\n2. Install `stitchee`, with its dependencies, by running the following from the repository directory:\n\n```shell\npoetry install\n```\n\n## How to test `stitchee` locally\n\n```shell\npoetry run pytest tests/\n```\n\n## Usage\n\n```shell\n$ poetry run stitchee --help\nusage: stitchee [-h] -o OUTPUT_PATH [--no_input_file_copies] [--keep_tmp_files] [--concat_method {xarray-concat,xarray-combine}] [--concat_dim CONCAT_DIM]\n                [--xarray_arg_compat XARRAY_ARG_COMPAT] [--xarray_arg_combine_attrs XARRAY_ARG_COMBINE_ATTRS] [--xarray_arg_join XARRAY_ARG_JOIN] [-O]\n                [-v]\n                path/directory or path list [path/directory or path list ...]\n\nRun the along-existing-dimension concatenator.\n\noptions:\n  -h, --help            show this help message and exit\n  --no_input_file_copies\n                        By default, input files are copied into a temporary directory to avoid modification of input files. This is useful for testing,\n                        but uses more disk space. By specifying this argument, no copying is performed.\n  --keep_tmp_files      Prevents removal, after successful execution, of (1) the flattened concatenated file and (2) the input directory copy if created\n                        by \'--make_dir_copy\'.\n  --concat_method {xarray-concat,xarray-combine}\n                        Whether to use the xarray concat method or the combine-by-coords method.\n  --concat_dim CONCAT_DIM\n                        Dimension to concatenate along, if possible. This is required if using the \'xarray-concat\' method\n  --sorting_variable SORTING_VARIABLE\n                        Name of a variable to use for sorting datasets before concatenation by xarray. E.g., \'time\'.\n  --xarray_arg_compat XARRAY_ARG_COMPAT\n                        \'compat\' argument passed to xarray.concat() or xarray.combine_by_coords().\n  --xarray_arg_combine_attrs XARRAY_ARG_COMBINE_ATTRS\n                        \'combine_attrs\' argument passed to xarray.concat() or xarray.combine_by_coords().\n  --xarray_arg_join XARRAY_ARG_JOIN\n                        \'join\' argument passed to xarray.concat() or xarray.combine_by_coords().\n  --group_delim GROUP_DELIM\n                        Character or string to use as group delimiter\n  -O, --overwrite       Overwrite output file if it already exists.\n  -v, --verbose         Enable verbose output to stdout; useful for debugging\n\nRequired:\n  path/directory or path list\n                        Files to be concatenated, specified via (1) multiple paths of the files to be concatenated, (2) single path to text\n                        file containing linebreak-separated paths of files to be concatenated, (3) single path to netCDF file to be copied to\n                        output path, or a (4) single directory containing the files to be concatenated.\n  -o OUTPUT_PATH, --output_path OUTPUT_PATH\n                        The output filename for the merged output.\n```\n\nFor example:\n\n```shell\npoetry run stitchee /path/to/netcdf/directory/ -o /path/to/output.nc\n```\n\n---\nThis package is NASA Software Release Authorization (SRA) # LAR-20433-1\n',
    'author': 'Daniel Kaufman',
    'author_email': 'daniel.kaufman@nasa.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nasa/stitchee',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
