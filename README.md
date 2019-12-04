# NBBinder - Jupyter Notebook Binder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/rmsrosa/nbbinder/NBBinder_Test) ![readthedocs badge](https://readthedocs.org/projects/nbbinder/badge/) ![GitHub repo size](https://img.shields.io/github/repo-size/rmsrosa/nbbinder)

NBBinder generates a navigable book-like structure to a collection of Jupyter notebooks.

## Description

This package comprises methods that read a collection of Jupyter notebooks from a given directory and

- add a **Table of Contents** to a selected notebook file, with links to the other notebooks;
- add a **Header** to each notebook, with custom informations;
- add, in the **header** and in the **footline** of each notebook, **navigator links**, to traverse  to the previous or the next notebook, and to other selected notebooks, such as the Table of Contents and the Bibliography;
- include, in the **header** of each notebook, a **Google Colab badge** and a **Binder badge**, with links to opening each notebook in these cloud computing plataforms (if the notebooks are hosted in github.com);
- **restructure** the notebooks, by automatically renaming the files, in case a new notebook is to be inserted in between other notebooks.

## Example

The most convenient way to use the module, or script, is via a configuration file. For instance, consider the following `config.yml`, in the same directory as the notebooks, and with the following content:

```yaml
directory:
  app_to_notes_path: nb_alice

book:
  toc_nb_name: 00.00-Alice's_Adventures_in_Wonderland.ipynb
  show_full_entry_in_toc: True
  header: "*[NBBinder test based on 'Alice's Adventures in Wonderland' chapter names](https://github.com/rmsrosa/nbbinder)*"
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
nbb.bind('config.yml')
```

Or we execute it as a script in the command line:

```bash
./nbbinder.py config.yml
```

If we call the `nbb.bind('config.yml')` from a different directory, we should add the parameter `directory` to the configuration file, with the path to the collection of notebooks.

Suppose we run the `nbb.bind('config.yml')`, with the above configuration file, in a directory with the following indexed notebooks:

```bash
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

We may have a glimpse of the result looking at a printscreen of the updated `00.00-Alice's_Adventures_in_Wonderland.ipynb`, with the table of contents, the header, and the footline:

[00.00-Alice's_Adventures_in_Wonderland.ipynb print screen](tests/nb_alice_toc.jpg)

More information on the [Documentation of the Project on readthedocs.org](https://nbbinder.readthedocs.io/en/latest/).

## License

The original work in [Python Data Science Handbook/tools](https://github.com/jakevdp/PythonDataScienceHandbook/tree/master/tools) is licensed by [Jake VanderPlas](http://vanderplas.com/), under the [MIT license](https://opensource.org/licenses/MIT).

The current modifications in this package is also provided under the [MIT license](https://opensource.org/licenses/MIT). See the file [LICENSE](LICENSE).
