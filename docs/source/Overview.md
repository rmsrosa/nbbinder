# Overview

**NBBinder** generates a navigable book-like structure to a collection of Jupyter notebooks.

## Description

The main method in this package is called `bind()`. It reads a collection of Jupyter notebooks from a given directory and

- add a **Table of Contents** to a selected notebook file, with links to the other notebooks;
- add a **header** to each notebook, with custom informations;
- add, in the **header** and in the **footline** of each notebook, **navigator links**, to traverse  to the previous or the next notebook, and to other selected notebooks, such as the Table of Contents and the Bibliography;
- include, in the **header** of each notebook, a **Google Colab badge** and a **Binder badge**, with links to opening each notebook in these cloud computing plataforms (if the notebooks are hosted in github.com);
- **restructure** the notebooks, by automatically renaming the files, in case a new notebook is to be inserted in between other notebooks.

## Methods

The main method in this package is called `bind()`. It restructures the notebooks if needed and adds the Table of Contents, header, and navigators from the data provided in the arguments.

The method `bind()` can be called in two different ways:

- **directly with the arguments** to be applied in the bindind process; or
- **with a configuration file** as argument, with the configuration file containing the desired arguments;

The `bind()` function calls the following functions in this module, which take care of each of the main features of the notebook binder:

- `restructure()`: reorder the notebooks when a new notebook is to be inserted between others;
- `add_contents()`: adds the Table of Contents to a selected "Contents" file;
- `add_headers()`: adds a header to each notebook with a given book info;
- `add_navigators()`: adds navigation bars to the top and bottom of each notebook.

Each of these later methods can be called separately, if only some of these features are desired.

When running `nbbinder.py` as a script, it expects the filename of the configuration file and calls the function `bind(config_file)`, where config_file is the name of the configuration file.

Look at the documentation for more information on each of these methods and for the other methods available on this package.

## Example

The most convenient way to use the module, or script, is via a configuration file. Consider, for instance, the configuration file `config_nb_alice.yml` used for testing the package and available in the subdirectory `tests` of the root directory:

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

Then, we import the module (in the same folder) and use the `bind()` method with this configuration file as argument:

```python
import nbbinder as nbb
nbb.bind('config_nb_alice.yml')
```

Or we execute it as a script in the command line:

```bash
./nbbinder.py config.yml
```

Notice, in the example configuration file above, the parameters `show_colab: True` and `show_binder: True`, and other parameters with the information about the github repository and directory where the notebooks in this package reside. This allows the module to add direct links for the corresponding notebooks to be opened in one of this cloud computing python environments.

**When opening the direct links from within the notebook-rendering of the github, it is necessary to click with the right button, otherwise nothing will be opened.**

The key `path_to_notes` indicates that the notebooks are in the folder `nb_alice`, relative to where the script is calling `bind()`. In this folder, one finds the following notebooks, properly indexed:

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
