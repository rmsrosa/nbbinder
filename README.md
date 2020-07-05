# Archived

Due to naming collision with [Binder](https://mybinder.org), this packaged has been archived and is survived by the renamed version [NBJoint](https://github.com/rmsrosa/nbjoint).

## NBBinder - Jupyter Notebook Binder

![Main Tests Workflow Status](https://github.com/rmsrosa/nbbinder/workflows/Main%20Tests/badge.svg) ![Flake8 Lint Test Workflow Status](https://github.com/rmsrosa/nbbinder/workflows/Flake8%20Lint%20Test/badge.svg) ![PDF Export Test Workflow Status](https://github.com/rmsrosa/nbbinder/workflows/PDF%20Export%20Test/badge.svg) ![readthedocs badge](https://readthedocs.org/projects/nbbinder/badge/)

![PyPI - Wheel](https://img.shields.io/pypi/wheel/nbbinder) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nbbinder)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![GitHub file size in bytes](https://img.shields.io/github/size/rmsrosa/nbbinder/nbbinder.py?label=module%20size) ![GitHub repo size](https://img.shields.io/github/repo-size/rmsrosa/nbbinder)

**NBBinder** generates a navigable book-like structure to a collection of Jupyter notebooks.

## Table of Contents

- [Description](#description)
- [Examples](#examples)
- [Installation](#installation)
- [Documentation](#documentation)
- [Development](#development)
- [Maintainer](#maintainer)
- [License](#license)

## Description

The main function in this module is called `bind()`. It reads a collection of Jupyter notebooks from a given directory and, upon configuration,

- adds a **table of contents** to a selected notebook file, with links to the other notebooks;

- adds a **header** cell to each notebook, with custom information about the collection of notebooks;

- adds a **badge** cell to each notebook, with links to opening the notebooks in different platforms or formats. For instance, one can include a **Google Colab badge** and a **Binder badge**, with links to opening each notebook in these cloud computing plataforms, a badge for showing **slides** as exported with `nbconvert`, and so on.

- adds **navigator links**, at the beggining and at the end of each notebook, with links to traverse to the previous and the next notebook, and to other selected notebooks, such as the Table of Contents and the References;

- **exports** the notebooks to other formats using `nbconvert`, so that, for example, **slides** can be generated automatically and in bulk.

## Examples

### A little taste

For instance, upon proper configuration (see section [Notebooks with slides and cloud computing badges](#notebooks-with-slides-and-cloud-computing-badges) below), the collection of bare notebooks in  the folder [Water bare collection](tests/nb_source/nb_water) is bound to the folder
[Water bound collection](tests/nb_builds/nb_water), and, in particular, the file [00.00-Water_Contents.ipynb](tests/nb_builds/nb_water/00.00-Water_Contents.ipynb) receives a table of contents, a header, navigator cells and the badges

[![Colab badge](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_water/00.00-Water_Contents.ipynb)[![My Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/rmsrosa/nbbinder/master?filepath=tests/nb_builds/nb_water/00.00-Water_Contents.ipynb)[![nbviewer](https://img.shields.io/badge/view%20in-nbviewer-orange)](https://nbviewer.jupyter.org/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_water/00.00-Water_Contents.ipynb)[![slides](https://img.shields.io/badge/view-slides-darkgreen)](https://nbviewer.jupyter.org/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_water_slides/00.00-Water_Contents.slides.html)

Below we show some examples in more details.

### Example with configuration file

The most convenient way to use the module, or script, is via a configuration file. The configuration files are written in the [YAML](https://en.wikipedia.org/wiki/YAML) format.

For instance, consider the following `config_nb_alice.yml`, which is included in the `tests` folder of the repository:

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

#### Notebook collection

The following collection of indexed notebooks is included in the folder `tests/nb_builds/nb_alice`:

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

#### Binding the collection

One way to bind the collection of notebooks is to import the module and use the `bind()` function with this configuration file as argument:

```python
import nbbinder as nbb
nbb.bind('config_nb_alice.yml')
```

Or we execute it as a script in the command line:

```bash
./nbbinder.py config_nb_alice.yml
```

In the `tests` directory, the configuration file is actually not in the same folder as the script. The collection is two folders down. This is indicated by the argument `path_to_notes: nb_builds/nb_alice`, given in the configuration file.

#### Result

After binding the notebooks in one of the two ways mentioned above, the following table of contents is inserted in the first notebook `00.00-Alice's_Adventures_in_Wonderland.ipynb`:

```text
Table of Contents
Alice's Adventures in Wonderland
1. Down the Rabbit-Hole
2. The Pool of Tears
3. A Caucus-Race and a Long Tale
4. The Rabbit Sends in a Little Bill
5. Advice from a Caterpillar
6. Pig and Pepper
7. A Mad Tea-Party
8. The Queen's Croquet-Ground
9. The Mock Turtle's Story
10. The Lobster Quadrille
11. Who Stole the Tarts?
12. Alice's Evidence
```

See [00.00-Alice's_Adventures_in_Wonderland.ipynb](tests/nb_builds/nb_alice/00.00-Alice's_Adventures_in_Wonderland.ipynb) for the actual bound version of the first notebook. Notice the **header** in the begining of the notebook and the **navigator** cells after the header and at the end of the notebook. Experiment with the navigator links to move to the other notebooks.

### Notebooks with subsections

By appropriately naming the files, we can have different formattings for the *Table of Contents*. For instance, if your list of files is

```text
00.00-Front_Page.ipynb
01.00-Introduction.ipynb
02.00-Project_Requirements.ipynb
03.00-The_History_of_Grammar.ipynb
04.00-Parts_of_Speech.ipynb
04.01-Nouns.ipynb
04.02-Verbs.ipynb
04.03-Adjectives.ipynb
04.04-Adverbs.ipynb
05.00-Sentences.ipynb
05.01-Complex_Sentences.ipynb
05.02-Compound_Sentences.ipynb
06.00-Paragraphs.ipynb
06.01-Descriptive.ipynb
06.02-Expository.ipynb
06.03-Narrative.ipynb
06.04-Persuasive.ipynb
07.00-Conclusion.ipynb
A0.00-Appendix.ipynb
BA.00-Glossary.ipynb
BB.00-Bibliography.ipynb
BC.00-Index.ipynb
```

we get, with a suitable configuration, the *Table of Contents*

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

See [00.00-Front-Page.ipynb](tests/nb_builds/nb_grammar_bound/00.00-Front_Page.ipynb) for the actual bound version of the first notebook.

The binder for the notebooks in this collection is configured to include *badges* to render, in [nbviewer](https://nbviewer.jupyter.org/), either the Jupyter notebook itself or the exported version to markdown. The *badge* cell is located just below the header. Just click the badge with the **mouse right button** to open it. If clicking it with the right button, from within github, nothing will happen.

### Notebooks with preheaders

This is particularly useful for lectures notes. For instance, by naming your collection of notebooks as

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

we get, with a suitable configuration, the *Table of Contents*

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

See [00.00-Introduction.ipynb](tests/nb_builds/nb_preheader/00.00-Introduction.ipynb) for the actual bound version of the first notebook.

Notice, above, different forms of displaying the parts of the same lecture note.

The binder for the notebooks in this collection is configured to include a *badge* to open them in [nbviewer](https://nbviewer.jupyter.org/). The *badge* is located just below the header. Just click the badge with the **mouse right button** to open it. If clicking it with the right button, from within github, nothing will happen.

## Notebooks with slides and cloud computing badges

The following configuration file is used in the collection of files present in the folder [Water](tests/source/nb_water):

```yaml
# Configuration file for the python module NBBinder

version: 0.13a

path_to_notes: nb_builds/nb_water

contents:
  toc_nb_name: 00.00-Water_Contents.ipynb
  toc_title: Table of Contents
  show_index_in_toc: True

header: "[*NBBinder test on a collection of notebooks about some thermodynamic properperties of water*](https://github.com/rmsrosa/nbbinder)"

navigators:
  core_navigators:
    - 00.00-Water_Contents.ipynb
    - BA.00-References.ipynb
  show_nb_title_in_nav: True
  show_index_in_nav: False

badges:
  - title: Open in Google Colab
    url: https://colab.research.google.com/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_water
    src: https://colab.research.google.com/assets/colab-badge.svg
  - title: Open in binder
    url: https://mybinder.org/v2/gh/rmsrosa/nbbinder/master?filepath=tests/nb_builds/nb_water
    src: https://mybinder.org/badge.svg
  - title: View in NBViewer
    url: https://nbviewer.jupyter.org/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_water
    label: view in
    message: nbviewer
    color: orange
  - title: View Slides
    url: https://nbviewer.jupyter.org/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_water_slides
    extension: .slides.html
    label: view
    message: slides
    color: darkgreen

exports:
  - export_path: nb_builds/nb_water_slides
    exporter_name: slides
    exporter_args:
      reveal_scroll: True
```

After binding the collection, the folder [Water bound collection](tests/nb_builds/nb_water) is created. See [00.00-Water_Contents.ipynb](tests/nb_builds/nb_water/00.00-Water_Contents.ipynb) for the first notebook, containing the table of contents. Now, each notebook has a badge cell with badges to open the notebooks in [Google Colab](https://colab.research.google.com/notebooks/intro.ipynb), [Binder](https://mybinder.org), and [nbviewer](https://nbviewer.jupyter.org/), and a final badge to open the associated [Reveal.JS](https://revealjs.com/) slides.

For the slides, the folder [Water Slides](tests/nb_builds/nb_water_slides) is created via [nbconvert](https://nbconvert.readthedocs.io/en/latest/), in accordance to the parameters associated with the key `exports` in the configuration file.

The **badge cell** looks like

[![Colab badge](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_water/00.00-Water_Contents.ipynb)[![My Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/rmsrosa/nbbinder/master?filepath=tests/nb_builds/nb_water/00.00-Water_Contents.ipynb)[![nbviewer](https://img.shields.io/badge/view%20in-nbviewer-orange)](https://nbviewer.jupyter.org/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_water/00.00-Water_Contents.ipynb)[![slides](https://img.shields.io/badge/view-slides-darkgreen)](https://nbviewer.jupyter.org/github/rmsrosa/nbbinder/blob/master/tests/nb_builds/nb_water_slides/00.00-Water_Contents.slides.html)

## Installation

The module is available in [PyPI](https://pypi.org/project/nbbinder/) and installation is done with

```bash
pip install nbbinder
```

The module can also be downloaded directly from github.com/rmsrosa/nbbinder.

More information about the installation processes on the [Installation section of the NBBinder documentation](https://nbbinder.readthedocs.io/en/latest/Installation.html).

## Documentation

The documentation of NBBinder is hosted on [nbbinder.readthedocs.io](https://nbbinder.readthedocs.io).

## Development

During the current alpha stage of the project, development is being done in the `master` branch, which is currently the only branch in the repository.

 When the first `beta` version is released, the latest stable version will stay in the `master` branch and development will belong to a separate `development` branch.

## Maintainer

[@rmsrosa](https://github.com/rmsrosa)

## License

The work in this package is licensed under the [MIT license](https://opensource.org/licenses/MIT).

This work is based on a few scripts in [Python Data Science Handbook/tools](https://github.com/jakevdp/PythonDataScienceHandbook/tree/master/tools), which is considered as the *original work*,  licensed by [Jake VanderPlas](http://vanderplas.com/) under the [MIT license](https://opensource.org/licenses/MIT).

See the file `LICENSE` in the root directory of the project.
