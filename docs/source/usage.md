# Basic Usage

## Numbering the collection of notebooks

NBBinder binds a collection of notebooks belonging to a specified directory.

In order to be processed, each notebook in the collection should start with a pair of *file numberings*, separated by a dot and followed by a dash.

Each file numbering is composed of two characters. We refer to each of the file numberings as `N1` and `N2`. Thus, a notebook should have the form

> `N1.N2-notebookfilename.ipynb`.

Each file numbering should be of one of the following forms:

- Two digits, from `00` to `99`;

- An uppercase letter followed by a digit, from `A0` to `Z9`;

- Two uppercase letters, from `AA` to `ZZ`.

Each file numbering is translated into a *head numbering*, for display in the table of contents and in the navigators.

The file numberings `N1` and `N2` are two hierarchical levels for the headings, such as "Chapter" and "Section", or "Section" and "Subsection".

The translation from file to heading numbering can be summarized in the following table:

| file numbering | heading numbering |
| --- | --- |
| `00` | |
| `01` to `09` | `1` to `9` |
| `10` to `99` | `10` to `99` |
| `A0` to `Z0` | `A` to `Z` |
| `A1` to `Z9` | `A1` to `Z9` |
| `AA` to `ZZ` | |

Notice that the file numbering `00` and the pure alphanumeric numberings `AA` to `ZZ` lead to an empty string, which means no heading numbering is shown in the table of contents. This is intended to allow `00` to be used for the *Front Matter* and `AA` to `ZZ` to be used for the *Back Matter*.

When used as the second level file numbering `N2`, the indices `AA` to `ZZ` can be used for non-numbering sections within chapters.

The file numberings `A0` to `Z0` are mainly intended to be used for the Appendices. The file numberings `A1` to `Z9` can also be used as such. They can appear either in the first level file numbering `N1` or in the second level `N2`.

There is an **exception** to the above translation rule, which is when first level `N1` is either `00` or any indice between `AA` and `ZZ`. In those cases, not only the first level heading number is an empty string, but the second as well, regardless of the value of `N2`. This is useful when the *Front Matter* is broken down into different notebooks. For example, instead of a single notebook

```text
00.00-Front_Matter.ipynb
```

with all the information for the *Front Matter*, we may have

```text
00.00-Title_Page.ipynb
00.01-Preface.ipynb
00.02-Foreword.ipynb
00.03-Table_of_Contents.ipynb
00.04-List_of_Abbreviations.ipynb
```

They will appear in the table of contents without any heading numbering. Just with the markdown title of each notebook (defined by the contents of the first heading `#` in the notebook).

We end this section with a translation table combining both levels `N1` and `N2`:

| file numberings N1.N2 | heading numbering |
| --- | --- |
| `00.00` to `00.ZZ` | Chapters with no heading number |
| `00.01` to `00.ZZ` | Sections with no heading number |
| `01.00` to `09.00` | Chapters `1` to `9` |
| `01.01` to `99.99` | Sections `1.1` to `99.99` |
| `01.A0` to `99.Z0` | Sections `1.A` to `99.A` |
| `01.AA` to `99.ZZ` | Sections `1` to `9` |
| `A0.00` to `Z0.00` | Chapters `A` to `Z` |
| `A0.01` to `Z0.99` | Sections `A.1` to `Z.99` |
| `A0.A0` to `Z0.Z0` | Sections `A.A` to `Z.Z` |
| `A0.AA` to `Z0.ZZ` | Sections `A` to `Z` |
| `A1.00` to `Z9.00` | Chapters `A1` to `Z9` |
| `A1.01` to `Z9.99` | Sections `A1.1` to `Z9.99` |
| `A1.A0` to `Z9.Z0` | Sections `A1.A` to `Z9.Z` |
| `A1.AA` to `Z9.ZZ` | Sections `A1` to `Z9` |
| `AA.01` to `ZZ.ZZ` | Sections with no heading number |

Some chapters and sections above have the same numbering. The difference between them is how they are indented in the table of contents.

## Numbering with preheaders

An extension to the previous numbering system is to allow for a preheader, so that we can write `Part 1`, `Chapter 1`, `Appendix A.1`, `Lecture 1`, and so on.

Preheaders are to be included by adding a dot between the file numbering `N2` and the dash. We can have one or two levels of preheaders. If there are two preheaders, another dot separates them. So we have the following options

> `N1.N2.Preheader1-notebookfilename.ipynb`

and

> `N1.N2.Preheader1.Preheader2-notebookfilename.ipynb`

They essentially work according to the following table

| file numbering | heading numbering |
| --- | --- |
| N1.N2.Preheader1 | Preheader1 N1.N2 |
| N1.N2.Preheader1.Preheader2 | Preheader N1. Preheader N2 |
| N1.N2..Preheader2 | Preheader N2 |

Notice the first case, in which `Preheader2` is empty, and compare it with the last case, in which `Preheader1` is empty. The first case includes both chapter and section numbers `N1` and `N2` in the heading numbers, which the last one only includes the section number.

In accordance with the rule when there is no preheader, no numbering is included when `N1` is an empty string, which no section numbering is included when only `N2` is empty.

Recalling the example in the [Overview](overview.md) section, suppose collection of notebooks is

```text
00.00-Introduction.ipynb
01.00.Lecture-Math_Background.ipynb
01.01-Vector_Calculus.ipynb
01.02-Rigid_Motions.ipynb
02.00.Lecture-Kinematics.ipynb
02.01.Lecture-Velocity_and_Acceleration.ipynb
02.02.Lecture-Different_Types_of_Motions_and_Their_Components.ipynb
03.00.Lecture-Dynamics.ipynb
03.01..Part-Force_and_Momentum.ipynb
03.02..Part-Orbits_of_Planets_and_Satellites.ipynb
03.03..Part-Interception_and_Rendezvous.ipynb
04.00.Lecture-Trajectory_Optimization.ipynb
04.01.Lecture.Part-Performance.ipynb
04.02.Lecture.Part-Gravity_Turn.ipynb
04.03.Lecture.Part-Optimization.ipynb
AA.00-References.ipynb
```

Then, the *Table of Contents* becomes

```text
Contents
Introduction
Lecture 1. Math Background
  1.1. Vector Calculus
  1.2. Rigid Motions
Lecture 2. Kinematics
  Lecture 2.1. Velocity and Acceleration
  Lecture 2.2. Different Types of Motions and Their Components
Lecture 3. Dynamics
  Part 1. Force and Momentum
  Part 2. Orbits of Planets and Satellites
  Part 3. Interception and Rendezvous
Lecture 4. Trajectory Optimization
  Lecture 4. Part 1. Performance
  Lecture 4. Part 2. Gravity Turn
  Lecture 4. Part 3. Optimization
References
```

Notice the different forms of subsectioning.

THE DOCUMENTATION IS OUTDATED FROM HERE ON

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
