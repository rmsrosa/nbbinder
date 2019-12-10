# NBBinder - Jupyter Notebook Binder

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/rmsrosa/nbbinder/NBBinder_Test) ![readthedocs badge](https://readthedocs.org/projects/nbbinder/badge/) ![PyPI - Wheel](https://img.shields.io/pypi/wheel/nbbinder) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nbbinder) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![GitHub repo size](https://img.shields.io/github/repo-size/rmsrosa/nbbinder)

**NBBinder** generates a navigable book-like structure to a collection of Jupyter notebooks.

## Description

The main function in this package is called `bind()`. It reads a collection of Jupyter notebooks from a given directory and, upon configuration,

- adds a **Table of Contents** to a selected notebook file, with links to the other notebooks;
- adds a **header** to each notebook, with custom informations;
- adds, in the **header** and in the **footline** of each notebook, **navigator links**, to traverse  to the previous or the next notebook, or to other selected notebooks, such as the Table of Contents and the Bibliography;
- insert, in the **header** of each notebook, a **Google Colab badge** and a **Binder badge**, with links to opening each notebook in these cloud computing plataforms (if the notebooks are hosted in github.com);
- **restructures** the notebooks, by automatically renaming the files, in case a new notebook is to be inserted in between other notebooks.

## Example

The most convenient way to use the module, or script, is via a configuration file. The configuration files are written in [YAML](https://en.wikipedia.org/wiki/YAML). For instance, consider the following `config_nb_alice.yml`:

```yaml
directory:
  path_to_notes: nb_alice

book:
  toc_nb_name: 00.00-Alice's_Adventures_in_Wonderland.ipynb
  show_full_entry_in_toc: True
  header: "[*NBBinder test on a collection of notebooks named after the chapters of 'Alice's Adventures in Wonderland'*](https://github.com/rmsrosa/nbbinder)*"
  core_navigators:
    - 00.00-Alice's_Adventures_in_Wonderland.ipynb
  user: rmsrosa
  repository: nbbinder
  branch: master
  github_nb_dir: tests/nb_alice
  show_colab: True
  show_binder: True
  show_full_entry_in_nav: False
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

Suppose we run the `nbb.bind('config_nb_alice.yml')`, with the above configuration file and with the following indexed notebooks in the subsubdirectory `nb_alice`:

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

More information on the [Documentation of NBBinder on readthedocs.org](https://nbbinder.readthedocs.io/en/latest/).

## Installation

The package can be installed from [PyPi](https://pypi.org/project/nbbinder/) with

```bash
pip install nbbinder
```

It can also be downloaded directly from github.com/rmsrosa/nbbinder.

More information on the [Documentation of NBBinder on readthedocs.org](https://nbbinder.readthedocs.io/en/latest/).

## License

The original work in [Python Data Science Handbook/tools](https://github.com/jakevdp/PythonDataScienceHandbook/tree/master/tools) is licensed by [Jake VanderPlas](http://vanderplas.com/), under the [MIT license](https://opensource.org/licenses/MIT).

The current modifications in this package is also provided under the [MIT license](https://opensource.org/licenses/MIT). See the file [LICENSE](LICENSE).
