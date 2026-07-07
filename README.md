# blocksnet

---

[![PyPi](https://badge.fury.io/py/blocksnet.svg)](https://badge.fury.io/py/blocksnet)
![License](https://img.shields.io/github/license/GeorgeKontsevik/blocksnet?style=flat&logo=opensourceinitiative&logoColor=white&color=blue)
[![OSA-improved](https://img.shields.io/badge/improved%20by-OSA-yellow)](https://github.com/aimclub/OSA)

Built with:

![numpy](https://img.shields.io/badge/NumPy-013243.svg?style={0}&logo=NumPy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style={0}&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikitlearn-F7931E.svg?style={0}&logo=scikit-learn&logoColor=white)
![sphinx](https://img.shields.io/badge/Sphinx-000000.svg?style={0}&logo=Sphinx&logoColor=white)
![tqdm](https://img.shields.io/badge/tqdm-FFC107.svg?style={0}&logo=tqdm&logoColor=black)

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

BlocksNet is a Python library for generating master plan requirements and related urban-area analyses from spatial data. It is aimed at researchers and developers working on urban planning, service planning, and geospatial analytics workflows. The repository centers on programmatic library use and also includes notebook-based examples that show an end-to-end pipeline for preparing blocks, assigning land use, and computing spatial relations. If you are new to the project, start with the getting started material and the example workflow to understand the intended usage pattern.

---

## Core Features

- Generates urban blocks from boundary and transport/water geometry, giving developers a base spatial unit for downstream planning workflows.
- Assigns land-use categories to blocks from functional-zone inputs, enabling rule-based urban classification and analysis.
- Builds city accessibility graphs and computes accessibility matrices, supporting travel-time based relations between blocks.
- Aggregates building information into block-level urban parameters, so population and building characteristics can be used in planning calculations.
- Supports notebook-driven, geospatial workflows with OpenStreetMap-backed data preparation, making it easier to prototype and inspect results interactively.

---

## Installation

**Prerequisites:** requires Python >=3.10

Install blocksnet using one of the following methods:

**Using PyPi:**

```sh
pip install blocksnet
```

---

## Getting Started

**Prerequisites**

- Python 3.10 or newer.
- The package depends on the libraries declared in `pyproject.toml`; optional documentation and notebook support are available through extras.

1. Install the package in editable mode.

```bash
   pip install -e .
```

2. If you plan to run the example notebook workflow or documentation build, install the documented extras.

```bash
   pip install -e '.[full,docs,ipynb]'
```

3. For notebook use, install the Jupyter kernel used in the documentation workflow.

```bash
   python -m pip install ipykernel
   python -m ipykernel install --user --name python3 --display-name "Python 3"
```

4. To sync the documentation example links, run the helper script from `docs/scripts`.

```bash
   python docs/scripts/sync_examples.py
```

5. Build the Sphinx documentation from the `docs` directory.

```bash
   sphinx-build docs/source docs/build
```

---

## Architecture

blocksnet is organized around a workflow for urban spatial analysis and planning. The example pipeline shows the main flow: urban boundaries and source geometries are prepared, blocks are cut from lines and polygons, land use is assigned to the resulting blocks, and then spatial relations such as accessibility matrices or graphs are computed.

On top of that core workflow, the library groups capabilities into several functional areas:

- **Blocks processing**: cutting, assignment, aggregation, classification, and postprocessing of urban blocks.
- **Relations**: accessibility, distance, and adjacency representations between blocks.
- **Analysis**: indicators and domain analyses for land use, network, geometry, services, provision, and related urban metrics.
- **Preprocessing and synthesis**: input preparation, imputation, and higher-level planning tasks such as land use planning, services planning, and network morphing.
- **Machine learning and optimization**: model training strategies and optimization components used by some analysis and planning workflows.

The repository also includes example notebooks and documentation, which suggest that these components are intended to be composed in notebook-driven or script-based research workflows rather than deployed as separate services.

---

## API Reference

The documented public entry points visible in the provided context are:

- `blocksnet.__version__` — package version, loaded from installed package metadata.
- `blocksnet.blocks.cutting.preprocess_urban_objects` — preprocesses urban object layers before block cutting.
- `blocksnet.blocks.cutting.cut_urban_blocks` — cuts urban blocks from a boundary and preprocessed geometry.
- `blocksnet.blocks.assignment.assign_land_use` — assigns land use to blocks using functional-zone rules.
- `blocksnet.relations.get_accessibility_graph` — builds a city graph for accessibility calculations.
- `blocksnet.relations.calculate_accessibility_matrix` — calculates an accessibility matrix for blocks and a graph.
- `blocksnet.enums.LandUse` — land-use enumeration used when defining assignment rules.

The repository context also shows a notebook-driven workflow in `examples/pipeline.ipynb` that uses these functions in sequence.

---

## Examples

Examples of how this should work and how it should be used are available [here](https://github.com/GeorgeKontsevik/blocksnet/tree/main/examples).

---

## Documentation

A detailed blocksnet description is available [here](https://aimclub.github.io/blocksnet/).

---

## Contributing

- **[Report Issues](https://github.com/GeorgeKontsevik/blocksnet/issues)**: Submit bugs found or log feature requests for the project.

- **[Submit Pull Requests](https://github.com/GeorgeKontsevik/blocksnet/tree/main/CONTRIBUTING.md)**: To learn more about making a contribution to blocksnet.

---

## License

This project is protected under the BSD 3-Clause "New" or "Revised" License. For more details, refer to the [LICENSE](https://github.com/GeorgeKontsevik/blocksnet/tree/main/LICENSE) file.

---

## Citation

If you use this software, please cite it as below.

### APA format:

    GeorgeKontsevik (2026). blocksnet repository [Computer software]. https://github.com/GeorgeKontsevik/blocksnet

### BibTeX format:

    @misc{blocksnet,

        author = {GeorgeKontsevik},

        title = {blocksnet repository},

        year = {2026},

        publisher = {github.com},

        journal = {github.com repository},

        howpublished = {\url{https://github.com/GeorgeKontsevik/blocksnet}},

        url = {https://github.com/GeorgeKontsevik/blocksnet}

    }

---