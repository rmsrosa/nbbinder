# NBBinder - Jupyter Notebook Binder

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/rmsrosa/nbbinder/NBBinder_Test) ![readthedocs badge](https://readthedocs.org/projects/nbbinder/badge/) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/nbbinder) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nbbinder) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![GitHub repo size](https://img.shields.io/github/repo-size/rmsrosa/nbbinder)

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
- adds a **header** to each notebook, with custom information about the collection of notebooks;
- adds a **badge** cell to each notebook, with a **Google Colab badge** and a **Binder badge**, with links to opening each notebook in these cloud computing plataforms (if the notebooks are hosted in github.com), and other custom badges, useful for showing **slides** as exported with `nbconvert`, and so on.
- adds **navigator links**, at the beggining and at the end of each notebook, with links to traverse to the previous and the next notebook, and to other selected notebooks, such as the Table of Contents and the References;

## Example

The most convenient way to use the module, or script, is via a configuration file. The configuration files are written in the [YAML](https://en.wikipedia.org/wiki/YAML) format. For instance, consider the following `config_nb_alice.yml` in the tests folder:

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
  user: rmsrosa
  repository: nbbinder
  branch: master
  github_nb_dir: tests/nb_builds/nb_alice
  show_colab: True
  show_binder: True
  show_custom_badge: True
  custom_badges:
    - name: markdown
      title: View Markdown
      url: https://github.com/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_alice_md
      replace_links: True
      label: view
      message: markdown
      color: blueviolet
    - name: nbviewer
      title: View in NBViewer
      url: https://nbviewer.jupyter.org/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_alice
      replace_links: False
      label: view in
      message: nbviewer
      color: orange
    - name: slides
      title: View Slides
      url: https://nbviewer.jupyter.org/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_alice_slides
      replace_links: True
      label: view
      message: slides
      color: darkgreen

exports:
  - export_path: nb_builds/nb_alice_slides
    exporter_name: slides
    exporter_args:
      reveal_scroll: True
  - export_path: nb_builds/nb_alice_md
    exporter_name: markdown
```

Then, we import the module (in the same folder) and use the `bind()` function with this configuration file as argument:

```python
import nbbinder as nbb
nbb.bind('config_nb_alice.yml')
```

Or we execute it as a script in the command line:

```bash
./nbbinder.py config_nb_alice.yml
```

Suppose we run the `nbb.bind('config_nb_alice.yml')`, with the above configuration file and with the following indexed notebooks in the subdirectory `nb_alice`:

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

Then, the following table of contents is inserted in the first notebook:

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

See [Markdown for 00.00-Alice's_Adventures_in_Wonderland](tests/nb_builds/nb_alice_md/00.00-Alice's_Adventures_in_Wonderland.md) for the markdown converted version of this notebook (experiment clicking on the badges with the mouse's right button to open the notebook in different renders and cloud computing platforms).

## Installation

The package can be installed from [PyPi](https://pypi.org/project/nbbinder/) with

```bash
pip install nbbinder
```

It can also be downloaded directly from github.com/rmsrosa/nbbinder.

More information on the installation processes on the [Installation section of NBBinder on readthedocs.org](https://nbbinder.readthedocs.io/en/latest/Installation.html)

## Documentation

More information on the [Documentation of NBBinder on readthedocs.org](https://nbbinder.readthedocs.io).

## Development

During the alpha stage, development is being done in the `master` branch, which is currently the only branch. When the first `beta` version is released, the latest stable version will stay in the `master` branch and development will belong to a separate `development` branch.

## Maintainer

[@rmsrosa](https://github.com/rmsrosa)

## License

The original work in [Python Data Science Handbook/tools](https://github.com/jakevdp/PythonDataScienceHandbook/tree/master/tools) is licensed by [Jake VanderPlas](http://vanderplas.com/), under the [MIT license](https://opensource.org/licenses/MIT).

The current modifications in this package is also provided under the [MIT license](https://opensource.org/licenses/MIT). See the file [LICENSE](LICENSE).
