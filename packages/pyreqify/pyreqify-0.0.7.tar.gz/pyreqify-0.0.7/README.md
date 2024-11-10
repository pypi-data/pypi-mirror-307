# PyReqify

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A lightweight Python module that efficiently extracts imported modules and generates a `requirements.txt` file with module versions for `.py` and `.ipynb` files in a given directory. Simplify dependency management for your projects!

## Features

- 📦 **Automatic Module Extraction**: Scans `.py` and `.ipynb` files in a directory to find all imported modules.
- 🔍 **Version Detection**: Fetches installed versions of imported modules (maps common aliases to official package names). It also gives the option to includes fetch `source python version` too.
- 📝 **Requirements Generation**: Creates a `requirements.txt` file with all extracted dependencies and the current Python version.


## Installation

Clone this repository and install the requirements.

```bash
pip install pyreqify
```


# ExtractPackages

## Usage
To use the `pyreqify` function and automatically create a `requirements.txt` file:

1. Place all `.py` and `.ipynb` files in a folder (e.g., `project`).
2. Run the function, which will generate a `requirements.txt` in the current directory with all extracted dependencies.

```python
pyreqify <source_folder> <destination folder> --include-source-pyversion
Example: pyreqify ~/Workspace/project . 
```