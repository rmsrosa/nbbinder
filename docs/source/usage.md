# Usage

**THIS DOCUMENTATION FILE IS OUTDATED**

## Indexing the collection of notebooks

In order to be processed, each notebook in the collection should start with an *index*, which is to be identified by a certain regular expression ending with a dash:

> `index-notebookname.ipynb`.

The main types of indices are the following:

- `'dd-notebookname.ipynb'`, where `'d'` is any decimal from 0 to 9;
- `'dd.dd-notebookname.ipynb'`, where `'d'` is as above;
- `'AX.-notebookname.ipynb'`, where `'A'` is the uppercase letter `'A'` and `'X'` is any uppercase letter, from `A` to `Z`;
- `'AX.dd-notebookname.ipynb'`, where the keys are as above;
- `'BX.-notebookname.ipynb'`, where `'B'` is the upper case letter `'B'` and `'X'` is as above; or
- `'BX.dd-notebookname.ipynb'`, where the symbols are as above.

The filenames go through a regular expressions matching operator and specific groups are extracted from them, as separated by the first dot.

- When the first group is `'00'`, the notebook appears in the beginning and is not numbered. It is for the **Front Matter**, e.g *Cover page*, *Copyright page*, *Dedication page*, *Epigraph*, *Table of Contents*, *Foreword*, *Preface*, *Acknowlegdments*, and so on.
- When the first group is from `'01'` to `'99'`, it is for the **Body** of the book, with the first group representing the chapter number and the second group, the section number. Except when the second group is either the empty string '' or `'00'`, in which cases there is no section number. These are useful for defining a *Part* of the book and an *Introduction to the Chapter*, respectively. Notice that the empty string '' comes before `'00'`.
- When the first group starts with `'A'`, it is assumed to be for an **Appendix**, in which the second letter `'X'` is the letter of the Appendix. The second group functions as the section of the Appendix, with the same exceptions as above in the cases in which the second group is either `''` or `'00'`.
- When the first group starts with `'B'`, the notebook appears at the end and is not numbered. It is for the non-numbered part of the **Back Matter**, such as  *Endnotes*, *Copyright permissions*, *Glossary*, *Bibliography*, *Index*, and so on.

The Table of Contents and the navigators follow the lexicographical order, so `''` < `'dd'` < `'AX'` < `'BX'`, for instance.

For more information about the different parts of a book, see [Parts of a Book Explained: Front Matter, Body, and Back Matter](https://blog.reedsy.com/front-matter-back-matter-book/).

Two further types of indices are used when it is desired to insert a notebook in between other notebooks. In this case, there are two more groups read by the regular expression, one before the first dot and the second before the dash. For instance,

- `'dd.dda-notebookname.ipynb'`, where `'a'` is one or more lower case characters. They indicate that this notebook should be renamed as `'dd.dd-notebookname.ipynb'`, and, if there is already a notebook with this index, its section number, along with the section number of subsequent notebooks, should be increased by one.
- `'dda.dd-notebookname.ipynb'`, where `'a'` is as above, and has a similar effect, but this time for the chapter number.
- Similarly for `'AXa...'` and `'BXa...'`.

These types of indices are only used by the `structure()` function. If the `structure()` is not called, or if the `bind()` function is called without the argument to structure the notebooks, then the notebooks with the above indices are **ignored**.

## Cell markers

The **Table of Contents**, the **headers**, and the **navigators** appear in selected cells in the jupyter notebooks. These cells have **markers**, according to their type.

The markers are **html** comments, so they do not show up in the notebook, except when editing the cell, although the point is precisely to avoid editing them and create and update them automatically through **NBBinder**.

The markers are

```text
<!--TABLE_OF_CONTENTS--\>

<!--HEADER-->

<!--NAVIGATOR-->
```

and their names speak for themselves.

The cell has to start with one of theses markers to be understood as the appropriate cell.

The **header** cell is always the first one in the notebook, when present.

The **navigator** cells appear in two places in each notebook: as the last cell, for the bottom navigators, and as either the first or the second cell, depending on whether there is a **header** cell or not.

The **Table of Contents** cell can vary in position. It can be given a priori at some place in the *Table of Contents* notebook file, or it can be inserted automatically by **NBBinder**. In the former case, the author of the notebook is responsible for opening up a cell and typing up the marker in the beginning of the cell. In the later case, **NBBinder** will create the table of contents in either the second to last cell, if there is a bottom **navigator**, or as the very last cell, otherwise. It must be stressed that the module will first look for the marker somewhere in the notebook and use the corresponding cell if it finds it. Only if it doesn't find it is that it will add a cell as the last or second to last cell.

If **NBBinder** is ran again, it will look for the marker cells and rewrite them with the updated information, removing any previous data.

**One *should not* add nor edit the markers for the *header* and the *navigators*, the code does that automatically.**

**One *can* add or edit the marker for the *table of contents* to place it in a specific positions, but this is *not necessary* since the code will insert one if it doesn't find it.**

## Restructuring the collection of notebooks

The function to insert a notebook in between other index notebooks is called `restructure()` and its definition starts with

```python
def restructure(path_to_notes='.'):
    ...
```

The `path_to_notes` is a non-required argument with the name of the folder in which the collection of notebooks is expected to be. It should be either an absolute path or a path relative to the current path in the script calling the function. If `path_to_notes` is not given, it is assumed to be the current directory.

This function reads all the Jupyter notebooks in the directory `path_to_notes` and look for those matching a regular expression indicating that the notebook is to be inserted in the collection. After that, it processes those notebooks accordingly.

## Creating the Table of Contents

The function to create, or update, the table of contents is called `add_contents()` and its definition starts with

```python
def add_contents(toc_nb_name, path_to_notes='.',
                 show_full_entry_in_toc=True):
    ...
```

The argument `toc_nb_name` is required and is the name of the jupyter notebook file in which the table of contents will be written.

The `path_to_notes` is as described above.

The last argument, `show_full_entry_in_toc`, determines whether the entries in the *Table of Contents* should start with the chapter and section numbers or not. The default is `True`, but in some cases, such as when one wants to have **Lecture 1** displayed instead of **1. Lecture**, it is useful to have this option and set it to `False`.

## Creating the headers

The function to create, or update, the headers is called `add_headers()` and its definition starts with

```python
def add_headers(header, path_to_notes='.'):
    ...
```

The argument `add_headers` is required and is a string with the header you want to see displayed on top of each notebook.

The `path_to_notes` is as described above.

## Creating the navigators

The function to create, or update, the navigator cells is called `add_navigators()` and its definition starts with

```python
def add_navigators(core_navigators=[], path_to_notes='.',
                   user = '', repository = '', branch = '',
                   github_nb_dir = '',
                   github_io_slides_dir = '',
                   show_colab=False, show_binder=False,
                   show_slides=False,
                   show_full_entry_in_nav=True):
    ...
```

There is no required argument.

Here is an explanation of the non-required arguments:

- `core_navigators` is a list of strings, where each element is the filename of a Jupyter notebook that you want to appear in the navigator bar, in between the links to the *previous* and the *next* notebooks. This is useful for direct links to the *Table of Contents* and the *Bibliography*, for instance. If it is not provided, it is assumed to be an empty list, and nothing is showed in between the links for the *previous* and *next* notebooks.

- `path_to_notes` is a non-required argument, as described above.

- `user` is the username of the owner of the github repository which the notebooks belong to, if they do belong to one. It defaults to a blank string.

- `repository` is the name of the github repository which the notebooks belong to, if they do belong to one. It defaults to a blank string.

- `branch` is the name of the associated branch in the github repository. It defaults to a blank string.

- `github_nb_dir` is the path to the notebooks from the root directory of the github repository.

- `github_io_slides_dir` is the directory in the `user.github.io` where the slides associated to the notebooks reside, if they exist. It defaults to a blank string.

- `show_colab` is a `boolean` argument informing the function whether to display the badge with the link to open up the notebook in [Google Colab](https://colab.research.google.com/notebooks/welcome.ipynb) environment in the "cloud". This works if the notebooks are in a github repository. It defaults to `False`.

- `show_binder` is a `boolean` argument informing the function whether to display the badge with the link to open up the notebook in the [binder](https://mybinder.org/) environment in the "cloud". This works if the notebooks are in a github repository. It defaults to `False`.

- `show_slides` is a `boolean` argument informing the function whether to display the badge with the link to open up the slides associated with each notebook, if they exist. This works if the slides are `user.github.io`, and the relative path to the root directory of `user.github.io` is to be provided by the argument `github_io_slides_dir` described above. It defaults to `False`.

- `show_full_entry_in_nav` indicates whether to display the chapter and section numbers in the navigation links along with the titles or just the titles. It defaults to `True`.

The colab, binder and slides links, when displayed, appear *above* the navigation bar in the top navigator cell and *below* the navigation bar in the bottom navigator cell, which I found to be more aesthetically pleasing.

**In the future, it is planned to allow the slides to reside in different sites. More customized badges might also be added.**

## Creating the book-like structure with all three elements

The function to **restructure** the notebooks and to create, or update, all the three elements (**table of contents**, **headers**, and **navigators**) at the same time is called `bind()`. This function simply calls the previous four functions, in the following order:

- `restructure(...)`
- `add_contents(...)`
- `add_headers(...)`
- `add_navigators(...)`

The function `bind()` can be called directly with the arguments for the other functions or with a single argument pointing to a configuration file, as described below.

## Creating the book-like structure from a configuration file

The easiest way to create/update the book-like structure of a collection of notebooks is by using a configuration file containing all the desired arguments.

The configuration file is expected to be in the [YAML](https://en.wikipedia.org/wiki/YAML) format, which is a human-readable, text file, which easily stores strings, integers, floating point numbers, booleans, lists, and dictionaries (and more). It is parsed to python via the [PyYAML](https://pyyaml.org/) module.

The function parses the configuration file to a python dictionary with one or more of the following keys:

- `directory`
- `restructure`
- `contents`
- `header`
- `navigator`
- `book`

The value of each key is another dictionary, containing the parameters for the associated function.

The order of the main keys is not important; the module takes care of them regardless. There are some rules used in the process:

- If `directory` is present, its value is send to the argument `path_to_notes`.
- If `restructure_notebooks` is present, the function `restructure()` is executed first.
- If `book` is present, the function `bind()` is executed, with the parameters given in this key.
- If `book` is not present, the other functions are executed, depending on whether the corresponding key is present, and in the following order:
  - `add_contents()`;
  - `add_headers()`; and
  - `add_navigators()`.
- Before either the `bind()` function or the separate `add_contents()`, `add_headers()`, and `add_navigators()` are executed, two functions are called to remove any header and navigator that might have been included in previous execution of the module, cleaning them up.

The key `directory` is not directly related to the configuration of the book-structure itself. It simply expects the configuration of the `path_to_notes` argument, so the script, module, or some specific functions within the module knows where to find the notebooks.

See the next section for an example of configuration file.

## Example of a configuration file

Here is the configuration file `config_nb_alice.yml` used for testing the package. It is  available in the subdirectory `tests` of the root directory of the repository.

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

## Binding the notebooks via the configuration file

Suppose the notebooks are in a subsubdirectory named `nb_alice`, as indicated by the key `path_to_notes`, in the configuration file. The indexed notebooks are the following:

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

Then, we import the module in a script in the folder `tests` and use the `bind()` function with the configuration file `config_nb_alice.yml` as argument:

```python
import nbbinder as nbb
nbb.bind('config_nb_alice.yml')
```

Or we execute it as a script in the command line:

```bash
./nbbinder.py config_nb_alice.yml
```

We may visualize the result looking at a printscreen of the updated `00.00-Alice's_Adventures_in_Wonderland.ipynb`, with the **table of contents**, the **header**, and the **navigators**:

![Screenshot of Alice's Adventures in Wonderland Jupyter notebook](nb_alice_toc.png)

## Binding the notebooks with arguments

Instead of using a configuration file, we may call `bind()` directly with the desired arguments:

```python
import nbbinder as nbb
nbb.bind(path_to_notes="nb_alice",
    toc_nb_name="00.00-Alice's_Adventures_in_Wonderland.ipynb",
    show_full_entry_in_toc=True,
    header="[*NBBinder test on a collection of notebooks named after the chapters of 'Alice's Adventures in Wonderland'*](https://github.com/rmsrosa/nbbinder)",
    core_navigators=[
        "00.00-Alice's_Adventures_in_Wonderland.ipynb"
        ],
    user='rmsrosa',
    repository='nbbinder',
    branch='master',
    github_nb_dir='tests/nb_alice',
    show_colab=True,
    show_binder=True,
    show_full_entry_in_nav=False)
```

## Binding the notebooks from a non-indexed notebook

We may also run **NBBinder** directly from a Jupyter notebook. It is preferred to run it from a non-indexed notebook, to avoid having it be altered by both the package and the jupyter kernel at the same time.

If the **NBBinder** package is installed in the environment, just import it as usual, otherwise, it can be imported with a relative path. This is achived by a code cell with the following code

```python
try:
    import nbbinder as nbb

except:
    import os
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), 'path', 'to', 'module')))

    import nbbinder as nbb
```

Then, in the same or in a different cell, we create the book-like structure with the following code:

```python
nbb.bind('config_nb_alice.yml')
```

This generates the following output cell:

```text
    * No markdown cell starting with <!--TABLE_OF_CONTENTS--> found in 00.00-Alice's_Adventures_in_Wonderland.ipynb
    - inserting table of contents in 00.00-Alice's_Adventures_in_Wonderland.ipynb
    - inserting header for 00.00-Alice's_Adventures_in_Wonderland.ipynb
    - inserting header for 01.00-Down_the_Rabbit-Hole.ipynb
    - inserting header for 02.00-The_Pool_of_Tears.ipynb
    - inserting header for 03.00-A_Caucus-Race_and_a_Long_Tale.ipynb
    - inserting header for 04.00-The_Rabbit_Sends_in_a_Little_Bill.ipynb
    - inserting header for 05.00-Advice_from_a_Caterpillar.ipynb
    - inserting header for 06.00-Pig_and_Pepper.ipynb
    - inserting header for 07.00-A_Mad_Tea-Party.ipynb
    - inserting header for 08.00-The_Queen's_Croquet-Ground.ipynb
    - inserting header for 09.00-The_Mock_Turtle's_Story.ipynb
    - inserting header for 10.00-The_Lobster_Quadrille.ipynb
    - inserting header for 11.00-Who_Stole_the_Tarts?.ipynb
    - inserting header for 12.00-Alice's_Evidence.ipynb
    - inserting navbar for 00.00-Alice's_Adventures_in_Wonderland.ipynb
    - inserting navbar for 01.00-Down_the_Rabbit-Hole.ipynb
    - inserting navbar for 02.00-The_Pool_of_Tears.ipynb
    - inserting navbar for 03.00-A_Caucus-Race_and_a_Long_Tale.ipynb
    - inserting navbar for 04.00-The_Rabbit_Sends_in_a_Little_Bill.ipynb
    - inserting navbar for 05.00-Advice_from_a_Caterpillar.ipynb
    - inserting navbar for 06.00-Pig_and_Pepper.ipynb
    - inserting navbar for 07.00-A_Mad_Tea-Party.ipynb
    - inserting navbar for 08.00-The_Queen's_Croquet-Ground.ipynb
    - inserting navbar for 09.00-The_Mock_Turtle's_Story.ipynb
    - inserting navbar for 10.00-The_Lobster_Quadrille.ipynb
    - inserting navbar for 11.00-Who_Stole_the_Tarts?.ipynb
    - inserting navbar for 12.00-Alice's_Evidence.ipynb
```

and *voilà*, the notebooks are bound.
