# NBBinder - Jupyter Notebook Binder

![Run Tests Workflow Status](https://github.com/rmsrosa/nbbinder/workflows/Run%20Tests/badge.svg)![readthedocs badge](https://readthedocs.org/projects/nbbinder/badge/)

![PyPI - Wheel](https://img.shields.io/pypi/wheel/nbbinder) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nbbinder)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![GitHub repo size](https://img.shields.io/github/repo-size/rmsrosa/nbbinder)

**NBBinder** generates a navigable book-like structure to a collection of Jupyter notebooks.

## Table of Contents

- [Description](#description)
- [Example](#example)
- [Installation](#installation)
- [Documentation](#documentation)
- [Development](#development)
- [Maintainer](#maintainer)
- [License](#license)

## Description

The main function in this package is called `bind()`. It reads a collection of Jupyter notebooks from a given directory and, upon configuration,

- adds a **Table of Contents** to a selected notebook file, with links to the other notebooks;
- adds a **header** cell to each notebook, with custom information about the collection of notebooks;
- adds a **badge** cell to each notebook, with a **Google Colab badge** and a **Binder badge**, with links to opening each notebook in these cloud computing plataforms (if the notebooks are hosted in github.com), and other custom badges, useful for showing **slides** as exported with `nbconvert`, and so on.
- adds **navigator links**, at the beggining and at the end of each notebook, with links to traverse to the previous and the next notebook, and to other selected notebooks, such as the Table of Contents and the References;

## Example

The most convenient way to use the module, or script, is via a configuration file. The configuration files are written in the [YAML](https://en.wikipedia.org/wiki/YAML) format.

### Example configuration file

For instance, consider the following `config_nb_alice.yml` in the tests folder:

```yaml
nbbversion: 0.7a

path_to_notes: nb_builds/nb_alice

contents:
  toc_nb_name: 00.00-Alice's_Adventures_in_Wonderland.ipynb
  toc_title: Table of Contents
  show_index_in_toc: True

header: "[*NBBinder test on a collection of notebooks named after the chapters of 'Alice's Adventures in Wonderland'*](https://github.com/rmsrosa/nbbinder)"

navigators:
  core_navigators:
    - 00.00-Alice's_Adventures_in_Wonderland.ipynb
  show_index_in_nav: False
  show_nb_title_in_nav: False

badges:
  custom_badges:
    - name: nbviewer
      title: View in NBViewer
      url: https://nbviewer.jupyter.org/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_alice
      extension: .ipynb
      replace_links: False
      label: view in
      message: nbviewer
      color: orange
    - name: pdf
      title: View PDF
      url: https://nbviewer.jupyter.org/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_alice_pdf
      extension: .pdf
      replace_links: True
      label: view
      message: PDF
      color: orange

exports:
  - export_path: nb_builds/nb_alice_pdf
    exporter_name: pdf
    exporter_args:
      latex_countInt: 1
```

### Notebook collection

The following collection of indexed notebooks is included in the folder `nb_alice` in the `tests` directory:

```text
00.00-Alice's_Adventures_in_Wonderland.ipynb
01.00-Down_the_Rabbit-Hole.ipynb
02.00-The_Pool_of_Tears.ipynb
03.00-A_Caucus-Race_and_a_Long_Tale.ipynb
04.00-The_Rabbit_Sends_in_a_Little_Bill.ipynb
05.00-Advice_from_a_Caterpillar.ipynb
06.00-Pig_and_Pepper.ipynb
07.00-A_Mad_Tea-Party.ipynb
08.00-The_Queen's_Croquet-Ground.ipynb
09.00-The_Mock_Turtle's_Story.ipynb
10.00-The_Lobster_Quadrille.ipynb
11.00-Who_Stole_the_Tarts?.ipynb
12.00-Alice's_Evidence.ipynb
```

### Binding the collection

One way to bind the collection of notebooks is to import the module and use the `bind()` function with this configuration file as argument:

```python
import nbbinder as nbb
nbb.bind('config_nb_alice.yml')
```

Or we execute it as a script in the command line:

```bash
./nbbinder.py config_nb_alice.yml
```

In the `tests` directory, the configuration file is actually not in the same folder as the collection, but two folders up. That is way the argument `path_to_notes: nb_builds/nb_alice` is given in the configuration file.

### Result

After binding the notebooks in one of the two ways mentioned above, the following table of contents is inserted in the first notebook `00.00-Alice's_Adventures_in_Wonderland.ipynb`:

## [Table of Contents](#/)

### [Alice's Adventures in Wonderland](#/)

### [1. Down the Rabbit-Hole](#/)

### [2. The Pool of Tears](#/)

### [3. A Caucus-Race and a Long Tale](#/)

### [4. The Rabbit Sends in a Little Bill](#/)

### [5. Advice from a Caterpillar](#/)

### [6. Pig and Pepper](#/)

### [7. A Mad Tea-Party](#/)

### [8. The Queen's Croquet-Ground](#/)

### [9. The Mock Turtle's Story](#/)

### [10. The Lobster Quadrille](#/)

### [11. Who Stole the Tarts?](#/)

### [12. Alice's Evidence](#/)

See [00.00-Alice's_Adventures_in_Wonderland](tests/nb_builds/nb_alice/00.00-Alice's_Adventures_in_Wonderland.ipynb) for the bound version of the first notebook. Experiment clicking on the badges with the mouse's right button to open the notebooks in [NBViewer](https://nbviewer.jupyter.org/) or to view the pdf of the notebooks. Experiment also the navigators to move to the other notebooks.

## Installation

The package can be installed from [PyPi](https://pypi.org/project/nbbinder/) with

```bash
pip install nbbinder
```

It can also be downloaded directly from github.com/rmsrosa/nbbinder.

More information about the installation processes on the [Installation section of NBBinder documentation](https://nbbinder.readthedocs.io/en/latest/Installation.html)

## Documentation

The documentation of NBBinder is hosted on [nbbinder.readthedocs.io](https://nbbinder.readthedocs.io).

## Development

During the current alpha stage of the project, development is being done in the `master` branch, which is currently the only branch in the repository.

 When the first `beta` version is released, the latest stable version will stay in the `master` branch and development will belong to a separate `development` branch.

## Maintainer

[@rmsrosa](https://github.com/rmsrosa)

## License

The original work in [Python Data Science Handbook/tools](https://github.com/jakevdp/PythonDataScienceHandbook/tree/master/tools) is licensed by [Jake VanderPlas](http://vanderplas.com/), under the [MIT license](https://opensource.org/licenses/MIT).

The current modifications in this package is also provided under the [MIT license](https://opensource.org/licenses/MIT). See the file [LICENSE](LICENSE).
