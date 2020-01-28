# Overview

**NBBinder** generates a navigable book-like structure to a collection of Jupyter notebooks.

## Description

The main function in this module is called `bind()`. It reads a collection of Jupyter notebooks from a given directory and, upon configuration,

- adds a **table of contents** to a selected notebook file, with links to the other notebooks;
- adds a **header** cell to each notebook, with custom information about the collection of notebooks;
- adds a **badge** cell to each notebook, with links to opening the notebooks in different platforms or formats. For instance, on can include a **Google Colab badge** and a **Binder badge**, with links to opening each notebook in these cloud computing plataforms (if the notebooks are hosted in github.com), a badge for showing **slides** as exported with `nbconvert`, and so on.
- adds **navigator links**, at the beggining and at the end of each notebook, with links to traverse to the previous and the next notebook, and to other selected notebooks, such as the Table of Contents and the References;

## Functions

The function `bind()` can be called in two different ways:

- *directly with the arguments* to be applied in the bindind process; or
- *with a configuration file* as argument, with the configuration file containing the desired arguments.

The `bind()` function calls the following functions in this module, which take care of each of the main features of the notebook binder:

- `reindex()`: reorder the notebooks when a new notebook is to be inserted between others or whether there are gaps in the indices;
- `add_contents()`: adds the Table of Contents to a selected "Contents" file;
- `add_headers()`: adds a header to each notebook with a given custom information;
- `add_badges()`: adds a badge cell to each notebook with one or more badges to open up the document in different platforms or formats;
- `add_navigators()`: adds navigation bars to the top and bottom of each notebook.

Each of these later functions can be called separately, if only some of these features are desired.

When running `nbbinder.py` as a script, it expects the filename of the configuration file and calls the function `bind(config_file)`, where config_file is the name of the configuration file.

Look at the documentation for more information on each of these functions and for the other functions available on this package.

## Example

The most convenient way to use the module, or script, is via a configuration file. The configuration files are written in the [YAML](https://en.wikipedia.org/wiki/YAML) format.

For instance, consider the following `config_nb_alice.yml` in the tests folder:

```yaml
# Configuration file for the python module NBBinder

version: 0.12a

path_to_notes: nb_builds/nb_alice

contents:
  toc_nb_name: 00.00-Alice's_Adventures_in_Wonderland.ipynb
  toc_title: Table of Contents
  show_index_in_toc: True

header: "NBBinder test on a collection of notebooks named after the chapters of 'Alice's Adventures in Wonderland'"

navigators:
  core_navigators:
    - 00.00-Alice's_Adventures_in_Wonderland.ipynb
  show_nb_title_in_nav: False
  show_index_in_nav: False
```

Then, we import the module and use the `bind()` function with this configuration file as argument:

```python
import nbbinder as nbb
nbb.bind('config_nb_alice.yml')
```

Or we execute it as a script in the command line:

```bash
./nbbinder.py config.yml
```

**When opening the direct links from within the notebook-rendering of the github, it is necessary to click the badges with the right button, otherwise nothing will be opened.**

The key `path_to_notes` indicates that the notebooks are in the folder `nb_builds/nb_alice`, relative to where the script that calls the function `bind()` is located. In this folder, one finds the following notebooks, properly indexed:

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

The function `bind()` then reads the notebooks and *binds* them accordingly.
