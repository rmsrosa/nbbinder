# Overview

**NBBinder** generates a navigable book-like structure to a collection of Jupyter notebooks.

## Description

The main function in this module is called `bind()`. It reads a collection of Jupyter notebooks from a given directory and, upon configuration,

- adds a **table of contents** to a selected notebook file, with links to the other notebooks;

- adds a **header** cell to each notebook, with custom information about the collection of notebooks;

- adds a **badge** cell to each notebook, with links to opening the notebooks in different platforms or formats. For instance, on can include a **Google Colab badge** and a **Binder badge**, with links to opening each notebook in these cloud computing plataforms, a badge for showing **slides** as exported with `nbconvert`, and so on.

- adds **navigator links**, at the beggining and at the end of each notebook, with links to traverse to the previous and the next notebook, and to other selected notebooks, such as the Table of Contents and the References;

- **exports** the notebooks to other formats using `nbconvert`, so that, for example, **slides** can be generated automatically and in bulk.

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
- `export_notebooks()`: exports the notebooks to any of the different formats as provided by [nbconvert](https://pypi.org/project/nbconvert/): HTML, LaTeX, PDF, Reveal JS, Markdown (md), ReStructured Text (rst), executable script. Notice that `add_badges()` can be used to link to the exported notebooks, useful, for instance, to access slides of the notebooks for presentation in class.

Each of these later functions can be called separately, if only some of these features are desired.

When running `nbbinder.py` as a script, it expects the filename of the configuration file and calls the function `bind(config_file)`, where config_file is the name of the configuration file.

Look at the documentation for more information on each of these functions and for the other functions available on this package.

## Example

The most convenient way to use the module, or script, is via a configuration file. The configuration files are written in the [YAML](https://en.wikipedia.org/wiki/YAML) format.

For instance, consider the following `config_nb_alice.yml`, which is included in the `tests` folder of the repository:

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

The function `bind()` then reads the notebooks and *binds* them accordingly. In particular, the following table of contents is added to the file indicated by the key `toc_nb_name` in the configuration file:

## [Table of Contents](#/)

### [Alice's Adventures in Wonderland](#/)

### [1. Down the Rabbit-Hole](#/)

### [2. The Pool of Tears](#/)

### [3. A Caucus-Race and a Long Tale](#/)

### [4. The Rabbit Sends in a Little Bill](#/)

### [5. Advice from a Caterpillar](#/)

### [6. Pig and Pepper](#/)

### [7. A Mad Tea-Party](#/)

### [8. The Queen's Croquet-Ground](#/)

### [9. The Mock Turtle's Story](#/)

### [10. The Lobster Quadrille](#/)

### [11. Who Stole the Tarts?](#/)

### [12. Alice's Evidence](#/)

The links above have been changed for display here, but in the actual table of contents they link to the corresponding notebook.

See [00.00-Alice's_Adventures_in_Wonderland.ipynb](tests/nb_builds/nb_alice/00.00-Alice's_Adventures_in_Wonderland.ipynb) for the bound version of the first notebook. Notice the **header** in the begining of the notebook and the **navigator** cells after the header and at the end of the notebook. Experiment with the navigator links to move to the other notebooks.

## Other examples

By appropriately naming the files, we can have different formattings for the *Table of Contents*. 

### Notebooks with subsections

For instance, if your list of files is

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
we get the *Table of Contents*

## [Table of Contents](#)

### [Front Page](#/)

### [1. Introduction](#/)

### [2. Project Requirements](#/)

### [3. The History of Grammar](#/)

### [4. Parts of Speech](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [4.1. Nouns](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [4.2. Verbs](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [4.3. Adjectives](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [4.4. Adverbs](#/)

### [5. Sentences](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [5.1. Complex Sentences](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [5.2. Compound Sentences](#/)

### [6. Paragraphs](06.00-Paragraphs.ipynb)

&nbsp;&nbsp;&nbsp;&nbsp; [6.1. Descriptive](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [6.2. Expository](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [6.3. Narrative](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [6.4. Persuasive](#/)

### [7. Conclusion](#/)

### [A. Appendix](#/)

### [Glossary](#/)

### [Bibliography](#/)

### [Index](#/)

As before, the links above have been changed for display here. See [00.00-Front-Page.ipynb](tests/nb_builds/nb_grammar_bound/00.00-Front_Page.ipynb) for the bound version of the first notebook.

### Notebooks for lecture notes

If your list of files is

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

we get the *Table of Contents*

## [Contents](#)

### [Introduction](#/)

### [Lecture 1. Math Background](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [1.1. Vector Calculus](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [1.2. Rigid Motions](#/)

### [Lecture 2. Kinematics](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [Lecture 2.1. Velocity and Acceleration](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [Lecture 2.2. Different Types of Motions and Their Components](#/)

### [Lecture 3. Dynamics](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [Part 1. Force and Momentum](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [Part 2. Orbits of Planets and Satellites](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [Part 3. Interception and Rendezvous](#/)

### [Lecture 4. Trajectory Optimization](04.00.Lecture-Trajectory_Optimization.ipynb)

&nbsp;&nbsp;&nbsp;&nbsp; [Lecture 4.Part 1. Performance](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [Lecture 4.Part 2. Gravity Turn](#/)

&nbsp;&nbsp;&nbsp;&nbsp; [Lecture 4.Part 3. Optimization](#/)

### [References](#/)

As before, the links above have been changed for display here. See [00.00-Introductino.ipynb](tests/nb_builds/nb_complement/00.00-Introduction.ipynb) for the bound version of the first notebook.

The binder for the notebooks in this collection is configured to include a *badge* to open them in [nbviewer](https://nbviewer.jupyter.org/). The *badge* is located just below the header. Just click the badge with the **mouse right button** for to open it. If clicking it with the right button, from within github, nothing will happen.
