# PyReqify

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![GitHub Badge](https://img.shields.io/badge/GitHub-Repo-blue.svg)](https://github.com/ammaryasirnaich/PyReqify)


A lightweight Python module for `requirements.txt generation`. It efficiently extracts imported modules and generates a `requirements.txt` file with module versions for `.py` and `.ipynb` files in a given directory. Simplify dependency management for your projects!




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
```

##### generated requirement.txt file
```

scikit-learn==1.5.1
keras==3.6.0
numpy==2.0.1
pandas==2.2.2
open3d==0.16.1
webcolors==24.8.0
nbformat==5.10.4
matplotlib==3.9.1
typing==3.7.4.3
torch==2.2.2
python==3.10.14
```


#### Examples
Example 1: Generate `requirements.txt` in the current working folder `without the Python version`.
```python
pyreqify ~/Workspace/project .
```

Example 2: Generate `requirements.txt` in the `deploy folder`, including the `Python version` in the file.
```python
pyreqify ~/Workspace/project ~/Workspace/project/deploy --include-source-pyversion
```

