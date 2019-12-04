# Usage

## Cell markers

The **Table of Contents**, the **headers**, and the **navigators** appear in selected cells in the jupyter notebooks. These cells have **markers**, according to their types.

The markers are **html** comments, so they do not show up in the notebook, except when editing the cell, although the point is precisely to avoid editing them and create and update them automatically.

The markers are

```html
<!--TABLE_OF_CONTENTS--\>

<!--HEADER-->

<!--NAVIGATOR-->
```

and their names speak for themselves.

The cell has to start with one of theses markers to be understood as the appropriate cell.

The **header** cell is always the first one in the notebook, when present.

The **navigator** cells appear in two places in each notebook: as the last cell, for the bottom navigators, and as either the first or the second cell, depending on whether there is a **header** cell or not.

The **Table of Contents** cell can vary in position. It can be given a priori at some place in the *Table of Contents* notebook file, or it can be included automatically by the `nbbinder` script. In the former case, the author of the notebook is responsible for opening up a cell and typing up the marker in the beginning of the cell. In the later case, the `nbbinder` module will create the table of contents in either the second to last cell, if there is a bottom **navigator**, or as the very last cell, otherwise. It must be stressed that the module will first look for the marker somewhere in the notebook and use the corresponding cell if it finds it. Only if it doesn't find it that it will add a cell as the last or second to last cell.

If the `nbbinder` script is ran again, it will look for the marker cells and rewrite them with the updated information, removing any previous data.

## Creating the Table of Contents

The method to create, or update, the table of contents is called `add_contents()` and its definition starts with

```python
def add_contents(toc_nb_name, app_to_notes_path='.',
                 show_full_entry_in_toc=True):
    ...
```

The argument `toc_nb_name` is required and is the name of the jupyter notebook file in which the table of contents will be written.

The `app_to_notes_path` is a non-required argument with the name of the folder in which both the `toc_nb_name` file and the collection of all notebooks to be listed in the table of contents are expected to be. It should be either an absolute path or a path relative to where the code is being ran. If `app_to_notes_path` is not given, it is assumed to be the current directory.

The last variable, `show_full_entry_in_toc`, determines whether the entries in the *Table of Contents* should start with the chapter and section numbers or not. The default is `True`, but in some cases, such as when one wants to have **Lecture 1** displayed instead of **1. Lecture**, it is useful to have this option and set it to `False`.

## Creating the headers

The method to create, or update, the headers is called `add_headers()` and its definition starts with

```python
def add_headers(header, app_to_notes_path='.'):
    ...
```

The argument `add_headers` is required and is a string with the header you want to be displayed on top of each notebook.

The `app_to_notes_path` is a non-required argument with the name of the folder in which both the `toc_nb_name` file and the collection of all notebooks to be listed in the table of contents are expected to be. It should be either an absolute path or a path relative from where the code is being ran. If `app_to_notes_path` is not given, it is assumed to be the current directory.

## Creating the navigators

The method to create, or update, the navigator cells is called `add_navigators()` and its definition starts with

```python
def add_navigators(core_navigators=[], app_to_notes_path='.',
                   repository = '', branch = '',
                   github_nb_dir = '',
                   show_colab=False, show_binder=False,
                   show_full_entry_in_nav=True):
    ...
```

There is no required argument.

Here is an explanation of the non-required arguments:

- `core_navigators` is a list of strings, where each element is the filename of a Jupyter notebook that you want to appear in the navigator bar, in between the links to the *previous* and the *next* notebooks. This is useful for direct links to the **Table of Contents** and the **Bibliography**, for instance. If it is not provided, it is assumed to be an empty list, and nothing is showed in between the links for the *previous* and *next* notebooks.

- `app_to_notes_path` is a non-required argument, with the name of the folder in which both the `toc_nb_name` file and the collection of all notebooks to be listed in the table of contents are expected to be. It should be either an absolute path or a path relative from where the code is being ran. If `app_to_notes_path` is not given, it is assumed to be the current directory.

- `repository` is the name of the github repository which the notebooks belong to, if they do belong to one. It defaults to a blank string.

- `branch` is the name of the associated branch in the github repository. It defaults to a blank string.

- `github_nb_dir` is the path to the notebooks from the root directory of the github repository.

- `show_colab` is a `boolean` argument informing the method whether to display the badge with the link to open up the notebook in [Google Colab](https://colab.research.google.com/notebooks/welcome.ipynb) environment in the "cloud". This works if the notebooks are in a github repository. It defaults to `False`.

- `show_binder` is a `boolean` argument informing the method whether to display the badge with the link to open up the notebook in the [binder](https://mybinder.org/) environment in the "cloud". This works if the notebooks are in a github repository. It defaults to `False`.

- `show_full_entry_in_nav` indicates whether to display the chapter and section numbers in the navigation links along with the titles or just the titles. It defaults to `True`.

The colab and binder links, when displayed, appear *above* the navigation bar in the top navigator cell and *below* the navigation bar in the bottom navigator cell, which I found to be more aesthetically pleasing.

## Creating the book-like structure with all three elements

The method to create, or update, all the three elements (**Table of Contents**, **headers**, and **navigators**) is called `bind()` and its definition starts with

```python
def bind(toc_nb_name, header, core_navigators,
         app_to_notes_path='.', repository='', branch='',
         github_nb_dir ='',
         show_colab=False, show_binder=False,
         show_full_entry_in_toc=True,
         show_full_entry_in_nav=True):
    ...
```

This method simply calls the previous three methods, in the following order:

- `add_contents(...)`
- `add_headers(...)`
- `add_navigators(...)`

Refer to the previous sections for each method and the nature of the required and non-required arguments.

## Creating the book-like structure from a configuration file

The easiest way to create/update the book-like structure of a collection of notebooks is by using a configuration file containing all the desired arguments (and elements).

The configuration file is expected to be in the [YAML](https://en.wikipedia.org/wiki/YAML) format, which is a human-readable, text file, which easily stores strings, integers, floating point numbers, booleans, lists, and dictionaries (and more). It is parsed to python via the [PyYAML](https://pyyaml.org/) module.

The method `bind_from_configfile(config_file)` expects the `config_file` to be parsed to a python dictionary with one or more of the following keys:

- `directory`
- `book`
- `contents`
- `header`
- `navigator`

The value of each key is another dictionary, containing the parameters for the associated method.

The order of the main keys is not important. The module takes care of them regardless. There are some rules to follow:

- If `book` is present, only the method `bind()` is executed, with the parameters given in this key.
- If `book` is not present, the other methods are executed, depending on whether the corresponding key is present, and in the following order: `add_contents()`, `add_headers()`, and `add_navigators()`.
- If neither `makebook`, nor `header` is present, a method is called to remove any header that was possibly added in a previous execution of the module.
- If neither `makebook`, nor `navigator` is present, a method is called to remove any navigator cell that was possibly added in a previous execution of the module.

The key `directory` is not directly related to the configuration of the book-structure itself. It simply expects the configuration of the `app_to_notes_path`, so the script, module, or some specific functions within the module know where to find the notebooks.

See the next section for examples of configuration files.

## Example of a configuration file

Here is the configuration file used for this specific set of lecture notes.

```yaml
book:
  toc_nb_name: 00.00-Front_Page.ipynb
  header: "*Header for the set of lecture notes in the nbbinder module*"
  core_navigators:
    - 00.00-Front_Page.ipynb
  repository: rmsrosa/nbbinder
  branch: master
  github_nb_dir: tests/lectures
  show_binder: True
  show_full_entry_in_toc: False
  show_full_entry_in_nav: False
```

## Running via a configuration file

Here we illustrate how we can build the book structure directly from a jupyter notebook.

This notebook is an indexed notebook, made to appear in the Table of Contents included in the [Front Page](00.00-Front_Page.ipynb). But it also alters the notebook itself, when adding or updating the header and the navigatores. This creates a conflict with the jupyter editor.

Hence, the best way is to have a non-indexed jupyter notebook which passes a configuration file to the `nbbinder` package. Being non-indexed, the notebook is not altered and there is no conflict with the jupyter editor. The notebook [Bind Notes](Bind_Notes.ipynb) accomplishes this goal.

Anyway, let us also execute the binder from here and see the conflict.

```python
import nbbinder as nbb
```

If it is not, and assuming this set of notebooks is two subdirectories down in the `nbbinder` package, with the structure

jupyternotebook/
    |
    |- jupyternotebook/
    |
    |- tests/
        |
        |- notebooks/
        |
        |- config1.yml
        |- :
        |- config5.yml

then we may import it with

```python
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..','..')))

import nbbinder as nbb
```

Then, considering that the configuration files are one folder up, we change the current directory there with

```python
os.chdir('..')
os.getcwd()
```

```bash
    /Users/rrosa/Documents/github_repositories
```

Then we create the book-like structure using one of the configuration files, say `config3.yml`.

```python
nbb.bind_from_configfile('config3.yml')
```

```txt
    - Table of contents updated in 00.00-Front_Page.ipynb
    - updating header for 00.00-Front_Page.ipynb
    - updating header for 00.01-Preface.ipynb
    - updating header for 00.90-Introduction.ipynb
    - updating header for 01.00-Methods_and_parameters.ipynb
    - updating header for 01.01-Cell_markers.ipynb
    - updating header for 01.02-Toc_creation.ipynb
    - updating header for 01.03-Header_creation.ipynb
    - updating header for 01.04-Navigator_creation.ipynb
    - updating header for 01.05-Book_creation.ipynb
    - updating header for 01.06-Configs_for_creation.ipynb
    - updating header for 01.07-Example_configs.ipynb
    - updating header for 02.00-Run_as_Module.ipynb
    - updating header for 02.01-Run_with_config.ipynb
    - updating header for 02.02-Run_with_arguments.ipynb
    - updating header for 03.00-Run_as_Script.ipynb
    - updating header for BA.00-References.ipynb
    - updating navbar for 00.00-Front_Page.ipynb
    - updating navbar for 00.01-Preface.ipynb
    - updating navbar for 00.90-Introduction.ipynb
    - updating navbar for 01.00-Methods_and_parameters.ipynb
    - updating navbar for 01.01-Cell_markers.ipynb
    - updating navbar for 01.02-Toc_creation.ipynb
    - updating navbar for 01.03-Header_creation.ipynb
    - updating navbar for 01.04-Navigator_creation.ipynb
    - updating navbar for 01.05-Book_creation.ipynb
    - updating navbar for 01.06-Configs_for_creation.ipynb
    - updating navbar for 01.07-Example_configs.ipynb
    - updating navbar for 02.00-Run_as_Module.ipynb
    - updating navbar for 02.01-Run_with_config.ipynb
    - updating navbar for 02.02-Run_with_arguments.ipynb
    - updating navbar for 03.00-Run_as_Script.ipynb
    - updating navbar for BA.00-References.ipynb
```

Once you do that, you need to either close the tab and reopen the notebook or click on `File > Reload Notebook from Disk`, in the top menu bar, in order to see the changes.

## Bind the Lecture Notes from a Non-Indexed notebook

If the `nbbinder` package is installed in the environment, just import it with as usual, otherwise, it is assumed this set of notebooks is two subdirectories down in the `nbbinder` package, so it can be imported with a relative path:

```python
try:
    import nbbinder as nbb

except:
    import os
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..', '..')))

    import nbbinder as nbb
```

Then we create the book-like structure from the configuration file `config.yml` contained in the same folder where these notebooks are:

```python
import os
os.chdir(os.path.join('tests', 'lectures'))
os.getcwd()
```

```bash
    /Users/rrosa/Documents/github_repositories/nbbinder/tests/lectures
```

```python
nbb.bind_from_configfile('config.yml')
```

```txt
    - Table of contents updated in 00.00-Front_Page.ipynb
    - updating header for 00.00-Front_Page.ipynb
    - updating header for 01.00-Cell_markers.ipynb
    - updating header for 02.00-Toc_creation.ipynb
    - updating header for 03.00-Header_creation.ipynb
    - updating header for 04.00-Navigator_creation.ipynb
    - updating header for 05.00-Book_creation.ipynb
    - updating header for 06.00-Configs_for_creation.ipynb
    - updating header for 07.00-Example_configs.ipynb
    - updating header for 08.00-Run_Config.ipynb
    - updating navbar for 00.00-Front_Page.ipynb
    - updating navbar for 01.00-Cell_markers.ipynb
    - updating navbar for 02.00-Toc_creation.ipynb
    - updating navbar for 03.00-Header_creation.ipynb
    - updating navbar for 04.00-Navigator_creation.ipynb
    - updating navbar for 05.00-Book_creation.ipynb
    - updating navbar for 06.00-Configs_for_creation.ipynb
    - updating navbar for 07.00-Example_configs.ipynb
    - updating navbar for 08.00-Run_Config.ipynb
```