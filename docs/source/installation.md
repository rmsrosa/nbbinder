# Installation

The package can be installed from [PyPi](https://pypi.org/project/nbbinder/) with

```bash
pip install nbbinder
```

It can also be downloaded directly from github.com/rmsrosa/nbbinder and installed, from the downloaded package directory, with

```bash
pip install .
```

If you do not wish to install the package, you can simply download it and import it as a local module as follows:

- If the subdirectory `nbbinder` of the project is in the same folder as the script that will import it, simply do

  ```python
  import nbbinder as nb
  ```

- If the subdirectory `nbbinder` is in a different location, use

  ```python
  import os
  import sys

  sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), 'path', 'from', 'script', 'to', 'module')))

  import nbbinder as nbb
  ```

In case of downloading the package and using it or installing it locally, you just need the file `nbbinder.py` in the root directory`.

