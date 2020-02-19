# Usage

## Numbering the collection of notebooks

**NBBinder** binds a collection of notebooks belonging to a specified directory.

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

> `00` => empty string
>
> `01` to `09` => `1` to `9`
>
> `10` to `99` => `10` to `99`
>
> `A0` to `Z0` => `A` to `Z`
>
> `A1` to `Z9` => `A1` to `Z9`
>
> `AA` to `ZZ` => empty string

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

> `00.00` to `00.ZZ` => Chapters with no heading number
>
> `00.01` to `00.ZZ` => Sections with no heading number
>
> `01.00` to `09.00` => Chapters `1` to `9`
>
> `01.01` to `99.99` => Sections `1.1` to `99.99`
>
> `01.A0` to `99.Z0` => Sections `1.A` to `99.A`
>
> `01.AA` to `99.ZZ` => Sections `1` to `9`
>
> `A0.00` to `Z0.00` => Chapters `A` to `Z`
>
> `A0.01` to `Z0.99` => Sections `A.1` to `Z.99`
>
> `A0.A0` to `Z0.Z0` => Sections `A.A` to `Z.Z`
>
> `A0.AA` to `Z0.ZZ` => Sections `A` to `Z`
>
> `A1.00` to `Z9.00` => Chapters `A1` to `Z9`
>
> `A1.01` to `Z9.99` => Sections `A1.1` to `Z9.99`
>
> `A1.A0` to `Z9.Z0` => Sections `A1.A` to `Z9.Z`
>
> `A1.AA` to `Z9.ZZ` => Sections `A1` to `Z9`
>
> `AA.01` to `ZZ.ZZ` => Sections with no heading number

Some chapters and sections above have the same numbering. The difference between them is how they are indented in the table of contents.

As an example, consider the following collection mentioned in the Section [Overview](overview.md):

```text
00.00-Front_Page.ipynb
02.00-Introduction.ipynb
04.00-Project_Requirements.ipynb
05.00-The_History_of_Grammar.ipynb
06.00-Parts_of_Speech.ipynb
06.02-Nouns.ipynb
06.03-Verbs.ipynb
06.05-Adjectives.ipynb
06.08-Adverbs.ipynb
08.00-Sentences.ipynb
08.01-Complex_Sentences.ipynb
08.03-Compound_Sentences.ipynb
09.00-Paragraphs.ipynb
09.01-Descriptive.ipynb
09.02-Expository.ipynb
09.03-Narrative.ipynb
09.04-Persuasive.ipynb
11.00-Conclusion.ipynb
AB.00-Appendix.ipynb
BA.00-Glossary.ipynb
BC.02-Bibliography.ipynb
BC.04-Index.ipynb
```

With the proper configuration, we obtain the *Table of Contents*

```text
Table of Contents
Front Page
1. Introduction
2. Project Requirements
3. The History of Grammar
4. Parts of Speech
  4.1. Nouns
  4.2. Verbs
  4.3. Adjectives
  4.4. Adverbs
5. Sentences
  5.1. Complex Sentences
  5.2. Compound Sentences
6. Paragraphs
  6.1. Descriptive
  6.2. Expository
  6.3. Narrative
  6.4. Persuasive
7. Conclusion
A. Appendix
Glossary
Bibliography
Index
```

## Numbering with preheaders

An extension to the previous numbering system is to allow for a preheader, so that we can write `Part 1`, `Chapter 1`, `Appendix A.1`, `Lecture 1`, and so on.

Preheaders are to be included by adding a dot between the file numbering `N2` and the dash. We can have one or two levels of preheaders. If there are two preheaders, another dot separates them. So we have the following options

> `N1.N2.Preheader1-notebookfilename.ipynb`

and

> `N1.N2.Preheader1.Preheader2-notebookfilename.ipynb`

They essentially work according to the following table

> `N1.N2.Preheader1` => `Preheader1 N1.N2.`
>
> `N1.N2.Preheader1.Preheader2.` => `Preheader N1. Preheader N2.`
>
> `N1.N2..Preheader2 => Preheader N2.`

Notice the first case, in which `Preheader2` is empty, and compare it with the last case, in which `Preheader1` is empty. The first case includes both chapter and section numbers `N1` and `N2` in the heading numbers, which the last one only includes the section number.

In accordance with the rule when there is no preheader, no numbering is included when `N1` is translated into an empty string, and no section numbering is included when `N2` is translated into an empty string.

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

## The binding process

Binding is achieved with the function `bind()`. Depending on the arguments given, this function calls the following functions, which take care of each of the main features of the notebook binder:

- `reindex()`: reorder the notebooks when a new notebook is to be inserted between others or whether there are gaps in the indices;
- `add_contents()`: adds the Table of Contents to a selected "Contents" file;
- `add_headers()`: adds a header to each notebook with a given custom information;
- `add_badges()`: adds a badge cell to each notebook with one or more badges to open up the document in different platforms or formats;
- `add_navigators()`: adds navigation bars to the top and bottom of each notebook.
- `export_notebooks()`: exports the notebooks to any of the different formats as provided by [nbconvert](https://pypi.org/project/nbconvert/): HTML, LaTeX, PDF, Reveal JS, Markdown (md), ReStructured Text (rst), executable script. Notice that `add_badges()` can be used to link to the exported notebooks, useful, for instance, to access slides of the notebooks for presentation in class.

The arguments to the function `bind()` can be given directly or via a configuration file.

A common argument to all these functions is `path_to_notes`, which is a string denoting the folder in which the notes are located. It is either an absolute path or a relative path from the script that calls `nbbinder.bind()`. The remaining arguments are for each of the functions above.

We can start explaining the arguments to `bind()` by the first statements defining the function:

```python
def bind(aux: str = None,
         path_to_notes: str = None,
         reindexing: list = None,
         contents: list = None,
         header: str = '',
         navigators: list = None,
         badges: list = None,
         exports: list = None,
         config_filename: str = None) -> None:
```

Except for `aux`, the aim of each of the arguments above are clear. Let us go through them in more detail, but leaving `aux` to the end.

- `path_to_notes`: string with the path to the collection of the notebooks.

- `reindexing`: dictionary with the following keys to be unpacked as arguments to the function `reindex()`:

  - `insert`: boolean saying whether or not to insert notebooks in the collection;

  - `tighten`: boolean saying whether or not to tighten the notebooks in the collection;

- `contents`: dictionary with the following keys to be unpacked as arguments to the function `add_contents()`:

  - `toc_nb_name`: string with the filename of the notebook in which the table of contents is to be inserted;

  - `toc_title`: string with a optional title to be placed in the start of the table of contents cell, such as "Table of Contents" or, in other languages, "Conteúdo", "Table des Matières", and so on;

  - `show_index_in_toc`: boolean saying whether or not to include the heading numbering in the table of contents.

- `header`: string with the text to be shown in the header cell.

- `navigators`: dictionary with the following keys to be unpacked as arguments to the function `add_navigators()`:

  - `core_navigators`: list of strings with the filenames of one or more notebooks to be added to the **navigator cells**, such as that containing the table of contents, and the bibliography;

  - `show_nb_title_in_nav`: boolean saying whether to display the name of the previous and the next notebooks in the collection or simply to display the words `previous` and `next;

  - `show_index_in_nav`: boolean saying whether to show the heading number along with the title of the previous and the next notebooks in the collection or just the title.

- `badges`: list of dictionaries with each dictionary containing the keys to generate each badge. Each badge is an html image link. The keys are

  - `title`: string that goes into the arguments `title` and `alt` of the html image tag `<img>`.

  - `url`: string with the `href` link argument of the html anchor tag `<a>` for the badge link;

  - `extension`: optional string with the extension that replaces the `.ipynb` extension when the badge directs to a page with a different format, for instance, to slides or markdown generated by the function `export_notebooks()`;

  - `src`: text with the url or local path to the badge image;

  - `label`, `message`, and `color`: strings to build the badges in [shields.io](https://shields.io/), which is used when `src` is not present.

- `exports`: list of dictionaries with each dictionary containing the keys to export the notebooks to different formats via [nbconvert](https://nbconvert.readthedocs.io/en/latest/):

  - `export_path`: string with the path where the exported files should be saved.

  - `exporter_name`: string with the name of the exporter as understood by the module `nbconvert`, for example `slides`, `html`, `markdown`, `latex`, `pdf`, and so on. See [nbconvert: supported output formats](https://nbconvert.readthedocs.io/en/latest/usage.html#supported-output-formats);

  - `exporter_args`: dictionary with extra arguments to be passed to `nbconvert`.

- `config_filename`: string with the absolute or relative path to the yaml configuration file.

- `aux`: Notice that all the arguments above are keyword arguments. But, in simple cases, to avoid writing down the keyword names `path_to_notes` or `config_filename`, the argument `aux` reads the first argument and checks whether it stands for a file or for a directory. If it is a file which ends with either `.yml` or `.yaml`, then `config_filename` takes the value of `aux`. If it is a directory, then `path_to_notes` takes the value of `aux`.

### Default values

It is easier to see the default values of the parameters above by looking at the beginning of each function:

```python
def reindex(path_to_notes: str = None,
            insert: bool = True,
            tighten: bool = False) -> None:
```

```python
def add_contents(path_to_notes: str = None,
                 toc_nb_name: str = None,
                 toc_title: str = '',
                 show_index_in_toc: bool = True) -> None:
```

```python
def add_headers(path_to_notes: str = None, header: str = None) -> None:
```

```python
def add_badges(path_to_notes: str = None, badges: list = None) -> None:
```

```python
def add_navigators(path_to_notes: str = None,
                   core_navigators: list = None,
                   show_nb_title_in_nav: bool = True,
                   show_index_in_nav: bool = True) -> None:
```

```python
def export_notebooks(path_to_notes: str = None,
                     export_path: str = None,
                     exporter_name: str = None,
                     exporter_args: dict = None) -> None:
```

## Configuration file

The easiest way to create/update the structure of a collection of notebooks is by using a configuration file containing all the desired arguments.

The configuration file is expected to be in the [YAML](https://en.wikipedia.org/wiki/YAML) format, which is a human-readable, text file, which easily stores strings, integers, floating point numbers, booleans, lists, and dictionaries (and more). It is parsed to python via the [PyYAML](https://pyyaml.org/) module.

The function parses the configuration file to a python dictionary. The expected keys are the following:

```yaml
# YAML configuration file for NBBinder

version:

path_to_notes:

reindexing:
  insert:
  tighten:

contents:
  toc_nb_name:
  toc_title:
  show_index_in_toc:

header:

badges:
  - title:
    url:
    extension:
    src:
    label:
    message:
    color:

navigators:
  core_navigators:
  show_nb_title_in_nav:
  show_index_in_nav:

exports:
  - export_path:
    export_name:
    exporter_args:
```

The keys `version` and `path_to_notes` are the **only mandatory ones**. The remaining keys are optional. The key `version` is checked for compatibility with the version of `nbbinder`.

The order of the main keys is not important; the module takes care of them regardless. There are some rules used in the process:

## Example of a configuration file

Here is the configuration file `config_nb_alice.yml` used for testing the package. It is available in the subdirectory `tests` of the root directory of the repository.

```yaml
# Configuration file for the python module NBBinder

version: 0.13a

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

## Binding via the configuration file

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

We may visualize the result looking at a printscreen of the updated `00.00-Alice's_Adventures_in_Wonderland.ipynb`:

![Screenshot of Alice's Adventures in Wonderland Jupyter notebook](nb_alice_toc.png)

## Binding via arguments

Instead of using a configuration file, we may call `bind()` directly with the desired arguments:

```python
nbb.bind(
    path_to_notes = 'nb_builds/nb_alice',
    contents={
        'toc_nb_name': "00.00-Alice's_Adventures_in_Wonderland.ipynb",
        'toc_title': 'Table of Contents',
        'show_index_in_toc': True
    },
    header="NBBinder test on a collection of notebooks named after the chapters of 'Alice's Adventures in Wonderland'",
    navigators={
        'core_navigators': [
            "00.00-Alice's_Adventures_in_Wonderland.ipynb"
        ],
        'show_nb_title_in_nav': False,
        'show_index_in_nav': False
    }
)
```

### Reindexing the notebooks

The function `reindex()` is useful when you want to include one (or more) notebooks in between two others or shift the notebooks around. Say we have the notebooks

```text
00.00-Front_Page.ipynb
01.00-Introduction.ipynb
02.00-Parts_of_Speech.ipynb
02.01-Nouns.ipynb
02.02-Adjectives.ipynb
02.03-Adverbs.ipynb
03.00-Sentences.ipynb
AA.00-Bibliography.ipynb
```

Suppose we want to add a new notebook `The_History_of_Grammar.ipynb` as Chapter 2 and a new notebook `Verbs.ipynb` as Section 2.2, moving up the other Chapters and Sections. For that, we write the notebook and name it with added character `&` in the proper place, depending whether it is to be a new chapter or a new section:

```text
00.00-Front_Page.ipynb
01.00-Introduction.ipynb
02&.00-The_History_of_Grammar.ipynb
02.00-Parts_of_Speech.ipynb
02.01-Nouns.ipynb
02.02&-Verbs.ipynb
02.02-Adjectives.ipynb
02.03-Adverbs.ipynb
03.00-Sentences.ipynb
AA.00-Bibliography.ipynb
```

Usually, the notebook with the character `&` is not recognized as an indexed notebook and is not included in the collection of notebooks to be bound. However, if `bind()` (or `reindex()`) is called with the argument `insert` as `True`, then the notebooks are renamed and the collection becomes

```text
00.00-Front_Page.ipynb
01.00-Introduction.ipynb
02.00-The_History_of_Grammar.ipynb
03.00-Parts_of_Speech.ipynb
03.01-Nouns.ipynb
03.02-Verbs.ipynb
03.03-Adjectives.ipynb
03.04-Adverbs.ipynb
04.00-Sentences.ipynb
AA.00-Bibliography.ipynb
```

If one wants to include two (or more) consecutive notebooks at a time, just add a lower case letter after `&`, say `&a`, `&b`, and so on.

Moreover, if we now want to move the Section "The History of Grammar" to an Appendix, we may rename `02.00-The_History_of_Grammar.ipynb` to `A0.00-The_History_of_Grammar.ipynb`. This leaves a gap in between Chapters 1 and 3:

```text
00.00-Front_Page.ipynb
01.00-Introduction.ipynb
03.00-Parts_of_Speech.ipynb
03.01-Nouns.ipynb
03.02-Verbs.ipynb
03.03-Adjectives.ipynb
03.04-Adverbs.ipynb
04.00-Sentences.ipynb
A0.00-The_History_of_Grammar.ipynb
AA.00-Bibliography.ipynb
```

Then, if `bind()` (or `reindex()`) is called with the argument `tighten` as `True`, the notebooks are renamed and the collection becomes

```text
00.00-Front_Page.ipynb
01.00-Introduction.ipynb
02.00-Parts_of_Speech.ipynb
02.01-Nouns.ipynb
02.02-Verbs.ipynb
02.03-Adjectives.ipynb
02.04-Adverbs.ipynb
03.00-Sentences.ipynb
A0.00-The_History_of_Grammar.ipynb
AA.00-Bibliography.ipynb
```

## Cell markers

The cells for the **Table of Contents**, the **headers**, the **badges**, and the **navigators** are marked with specific *html comments*, so they do not show up when the cells are rendered, except when editing the cell. The **markers** are automatically included by the module.

Except for the **Table of Contents**, **NBBinder** automatically removes any previous marked cell for cleaning up purposes. In particular, the location of these other marked cells are always the same. As for the **Table of Contents**, however, only its contents is deleted. If you desire to add the **Table of Contents** in a particular place inside a notebook, just add the marker to that place, or move a previously generated **Table of Contents** to the desired position.

The markers are python constants and are given as

```python
TOC_MARKER = "<!--TABLE_OF_CONTENTS-->"

HEADER_MARKER = "<!--HEADER-->"

BADGES_MARKER = "<!--BADGES-->"

NAVIGATOR_MARKER = "<!--NAVIGATOR-->"
```

Their names speak for themselves.

The cell has to start with one of theses markers to be understood as the appropriate cell.

The **header** cell is always the first one in the notebook, when present.

The **navigator** cells appear in two places in each notebook: as the last cell, for the bottom navigators, and as either the first or the second cell, depending on whether there is a **header** cell or not.

The **Table of Contents** cell can vary in position. It can be given a priori at some place in the notebook file, or it can be inserted automatically by **NBBinder**. In the former case, the author of the notebook is responsible for opening up a cell and typing up the marker in the beginning of the cell, or just wait for the first run of nbbinder to place it in the standart position and them move it somewhere else. The standart position set up by **NBBinder** is either the second to last cell, if there is a bottom **navigator** cell, or as the very last cell, otherwise. It must be stressed that the module will first look for the marker somewhere in the notebook and use the corresponding cell if it finds it. Only if it doesn't find it is that it will add a cell as the last or second to last cell.
