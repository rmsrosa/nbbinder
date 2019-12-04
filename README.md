# NBBinder - Jupyter Notebook Binder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![readthedocs badge](https://readthedocs.org/projects/nbbinder/badge/) ![GitHub repo size](https://img.shields.io/github/repo-size/rmsrosa/nbbinder)

NBBinder generates a navigable book-like structure to a collection of Jupyter notebooks.

## Description

This package comprises methods that read a collection of Jupyter notebooks from a given directory and

- add a **Table of Contents** to a selected notebook file, with links to the other notebooks;
- add a **Header** to each notebook, with custom informations;
- include, in the **header** of each notebook, a **Google Colab badge** and a **Binder badge**, with links to opening each notebook in these cloud computing plataforms;
- add, in the **header** and in the **footline** of each notebook, **navigator links**, to traverse  to the previous or the next notebook, and to other selected notebooks, such as the Table of Contents and the Bibliography;
- **restructure** the notebooks, by automatically renaming the files, in case a new notebook is to be included in between already numbered notebooks.

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

### A collection of notebooks

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

This inserts the following Table of Contents in the `00.00-Alice’s_Adventures_in_Wonderland.ipynb` notebook, which is the file indicated in the key `toc_nb_name`, in the `config.yml` file:

```markdown

```

### Table of Contents

The result

## Colab and Binder links

Notice, in the example configuration file above, the parameters `show_colab: True` and `show_binder: True`, and other parameters with the information about the github repository and directory where the notebooks in this package reside. This allows the module to add direct links for the corresponding notebooks to be opened in one of this cloud computing python environments.

When opening the direct links from within the notebook-rendering of the github, it is necessary to click with the right button, otherwise nothing will be opened.

## License

The original work in [Python Data Science Handbook/tools](https://github.com/jakevdp/PythonDataScienceHandbook/tree/master/tools) is licensed by [Jake VanderPlas](http://vanderplas.com/), under the [MIT license](https://opensource.org/licenses/MIT).

The current modifications in this package is also provided under the [MIT license](https://opensource.org/licenses/MIT). See the file [LICENSE](LICENSE).
