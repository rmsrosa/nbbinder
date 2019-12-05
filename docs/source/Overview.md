# Overview

## Description

NBBinder generates a navigable book-like structure to a collection of Jupyter notebooks.

It comprises methods that read a collection of Jupyter notebooks from a given directory and

- add a **Table of Contents** to a selected notebook file, with links to the other notebooks;
- add a **header** to each notebook, with custom informations;
- add, in the **header** and in the **footline** of each notebook, **navigator links**, to traverse  to the previous or the next notebook, and to other selected notebooks, such as the Table of Contents and the Bibliography;
- include, in the **header** of each notebook, a **Google Colab badge** and a **Binder badge**, with links to opening each notebook in these cloud computing plataforms (if the notebooks are hosted in github.com);
- **restructure** the notebooks, by automatically renaming the files, in case a new notebook is to be inserted in between other notebooks.

## Notebooks

In order to be processed, each notebook in the collection should start with an *index*, which is to be identified by a certain regular expression ending with a dash:

> `index-notebookname.ipynb`.

The main types of indices are the following:

- `'dd-notebookname.ipynb'`, where `'d'` is any decimal from 0 to 9;
- `'dd.dd-notebookname.ipynb'`, where `'d'` is as above;
- `'AX.-notebookname.ipynb'`, where `'A'` is the uppercase letter `'A'` and `'X'` is any uppercase letter, from `A` to `Z`;
- `'AX.dd-notebookname.ipynb'`, where the keys are as above;
- `'BX.-notebookname.ipynb'`, where `'B'` is the upper case letter `'B'` and `'X'` is as above; or
- `'BX.dd-notebookname.ipynb'`, where the symbols are as above.

The filenames go through a regular expressions matching operator and specific groups are extracted from them, as separated by the first two dots.

- When the first group is `'00'`, the notebook appears in the beginning and is not numbered. It is for the **Front Matter**, e.g *Cover page*, *Copyright page*, *Dedication page*, *Epigraph*, *Table of Contents*, *Foreword*, *Preface*, *Acknowlegdments*, and so on.
- When the first group is from `'10'` to `'99'`, it is for the **Body** of the book, with the first group representing the chapter number and the second group, the section number. Except when the second group is either the empty string '' or `'00'`, in which cases there is no section number. These are useful for defining a *Part* of the book and an introduction to the chapter, respectively. Notice that the empty string '' comes before `'00'`.
- When the first group starts with `'A'`, it is assumed to be for an **Appendix**, in which the second letter `'X'` is the letter of the Appendix. The second group functions as the section of the Appendix, with the same exceptions as above in the cases in which the second group is either `''` or `'00'`.
- When the first group starts with `'B'`, the notebook appears at the end and is not numbered. It is for the non-numbered part of the **Back Matter**, such as  *Endnotes*, *Copyright permissions*, *Glossary*, *Bibliography*, *Index*, and so on.

The Table of Contents and the navigators follow the lexicographical order, so `''` < `'dd'` < `'AX'` < `'BX'`, for instance.

Two further types of indices are used when it is desired to insert a notebook in between other notebooks. In this case, there are two more groups read by the regular expression, one before the first dot and the second before the dash. For instance,

- `'dd.dda-notebookname.ipynb'`, where `'a'` is one or more lower case characters. They indicate that this notebook should be renamed as `'dd.dd-notebookname.ipynb'`, and, if there is already a notebook with this index, then its section number, along with the section number of subsequent notebooks, should be increased by one.
- `'dda.dd-notebookname.ipynb'`, where `'a'` is as above, and has a similar effect, but this time for the chapter number.
- Similarly for `'AXa...'` and `'BXa...'`.

For more information about the structure of a book, see [Parts of a Book Explained: Front Matter, Body, and Back Matter](https://blog.reedsy.com/front-matter-back-matter-book/).

## Methods

The two main methods in this module are

- `bind()`: adds the Table of Contents, header, and navigators from the data provided in the arguments.
- `bind_from_configfile()`: adds the Table of Contents, header, and navigators from the data stored in a YAML configuration file given as argument.
The latter function simply reads the parameters from the configuration file and passes them to the `bind()` function.

The `bind()` function calls the following functions in this module, which take care of each of the main features of the notebook binder:

- `restructure()`: reorder the notebooks when a new notebook is to be inserted between others;
- `add_contents()`: adds the Table of Contents to a selected "Contents" file;
- `add_headers()`: adds a header to each notebook with a given book info;
- `add_navigators()`: adds navigation bars to the top and bottom of each notebook.

Each of these later methods can be called separately, if only some of these features are desired.

When running `nbbinder.py` as a script, it expects the filename of the configuration file and calls the function `bind_from_configfile(config_file)`, where config_file is the name of the configuration file.

Look at the documentation for more information on each of these methods and for the other methods available on this package.

## Example

The most convenient way to use the module, or script, is via a configuration file. Say we have a configuration file called `config.yml`, in the same directory as the notebooks, and with the following content:

```yaml
book:
  toc_nb_name: 00.00-Front_Page.ipynb
  header: "[*Header for the notebooks in the nbbinder module*](https://github.com/rmsrosa/nbbinder)"
  core_navigators:
    - 00.00-Front_Page.ipynb
    - BA.00-References.ipynb
  user: rmsrosa
  repository: nbbinder
  branch: master
  github_nb_dir: tests/notebooks
  show_colab: True
  show_binder: True
  show_full_entry_in_nav: False
```

Then, we import the module (in the same folder) and use the `bind()` method with this configuration file as argument:

```python
import nbbinder as nbb
nbb.bind('config.yml')
```

Or we execute it as a script in the command line:

```bash
./nbbinder.py config.yml
```

If we call the `nbb.bind('config.yml')` from a different directory, we should add the parameter `directory` to the configuration file, with the path to the collection of notebooks.

Notice, in the example configuration file above, the parameters `show_colab: True` and `show_binder: True`, and other parameters with the information about the github repository and directory where the notebooks in this package reside. This allows the module to add direct links for the corresponding notebooks to be opened in one of this cloud computing python environments.

**When opening the direct links from within the notebook-rendering of the github, it is necessary to click with the right button, otherwise nothing will be opened.**
