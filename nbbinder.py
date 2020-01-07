#!/usr/bin/env python3
"""
**NBBinder** generates a navigable book-like structure
to a collection of Jupyter notebooks.
"""

__author__ = "Ricardo M. S. Rosa <rmsrosa@gmail.com>"
__homepage__ = "http://github.com/rmsrosa/nbbinder"
__copyright__ = """Modified work Copyright (c) 2019 Ricardo M S Rosa
Original work Copyright (c) 2016 Jacob VanderPlas
"""
__license__ = "MIT"
__version__ = "0.7a5"

import os
import re
import itertools
import sys
import logging

from typing import Iterable

import yaml

import nbformat
from nbformat.v4.nbbase import new_markdown_cell

from nbconvert import exporters

# Regular expression for indexing the notebooks
# First tested in https://regexr.com/ (which is not the same as in python)
# then testeed with `re` library

IDX_GRP1 = r'(\d{2}|\b[A][A-Z]|\b[B][A-Z])'
IDX_GRP2 = r'(\d{2}|\b[A][A-Z]|\b[B][A-Z]|)'
MAIN_GRP = r'([^\)]*|[^\)]*\([^\)]*\)[^\)]*)'
EXT_GRP = r'(\.ipynb\b)'
INS_GRP = r'([a-z]|)'
MD_HTML_GRP = r'(\]\()'

REG = re.compile(r'\b' + IDX_GRP1 + r'\.' + IDX_GRP2 + r'-'
                 + MAIN_GRP + EXT_GRP)
REG_INSERT = re.compile(r'\b' + IDX_GRP1 + INS_GRP + r'\.'
                        + IDX_GRP2 + INS_GRP + r'-'
                        + MAIN_GRP + EXT_GRP)
REG_LINK = re.compile(MD_HTML_GRP + IDX_GRP1 + r'\.'
                      + IDX_GRP2 + r'-'
                      + MAIN_GRP + EXT_GRP)

# Markers for the affected notebook cells
TOC_MARKER = "<!--TABLE_OF_CONTENTS-->"
HEADER_MARKER = "<!--HEADER-->"
BADGES_MARKER = "<!--BADGES-->"
NAVIGATOR_MARKER = "<!--NAVIGATOR-->"

# Navigator templates
PREV_TEMPLATE = "[<- {title}]({url}) "
CENTER_TEMPLATE = "| [{title}]({url}) "
NEXT_TEMPLATE = "| [{title} ->]({url})"

# Link templates for the badges
COLAB_LINK = """<a href="https://colab.research.google.com/github/{user}/{repository}/blob/{branch}/{github_nb_dir}/{notebook_filename}"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Google Colab" title="Open in Google Colab"></a>
"""
BINDER_LINK = """<a href="https://mybinder.org/v2/gh/{user}/{repository}/{branch}?filepath={github_nb_dir}/{notebook_filename}"><img align="left" src="https://mybinder.org/badge.svg" alt="Binder" title="Open in binder"></a>
"""
CUSTOM_BADGE_LINK = """<a href="{badge_url}/{badge_filename}"><img align="left" src="https://img.shields.io/badge/{badge_label}-{badge_message}-{badge_color}" alt="{badge_alt}" title="{badge_title}"></a>
"""

# Metadata to flag cells for the slides
SLIDE_SHOW = {
    "slideshow": {
        "slide_type": "slide"
    }
}

SLIDE_SKIP = {
    "slideshow": {
        "slide_type": "skip"
    }
}


def indexed_notebooks(path_to_notes: str = '.') -> list:
    """Returns a sorted list with the filenames of the "indexed notebooks".

    The notebooks are expected to be in the folder indicated by the
    argument `path_to_notes`. The "indexed notebooks" are those that
    match the regular expression REG. Filenames that do not
    match the regular expression are ignored.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    Returns
    -------
    : list of str
        A list with the filenames of the notebooks that match
        the regular expression (the "indexed notebooks"),
        ordered by the lexicographycal order.
    """
    return sorted(nb for nb in os.listdir(path_to_notes) if REG.match(nb))


def is_index(idx: str) -> bool:
    """Checks whether a string is an index, returning True or False.

    An index is a string of length two, composed either of two numeric
    characters or starting with the uppercase letters 'A' and 'B'
    and ending with either a numeric character or an uppercase letter.

    Parameters
    ----------
    idx : str
        The two character long string with the index.

    Returns
    -------
    : bool
        True or False depending whether g is an index or not.
    """

    if isinstance(idx, str) and len(idx) == 2:
        if ((idx[0].isdecimal() or idx[0] in ('A', 'B'))
                and (idx[1].isdecimal() or idx[1].isupper())):
            return True

    return False


def increase_index(idx: str) -> str:
    """Increases an index by one.

    If the index is numeric, in the range '00' to '98', it returns
    an index in the range '01' to '99'.

    If the index is alphanumeric, in the range 'A0' to 'A8',
    or 'B0' to 'B8', it returns an index in the range 'A1' to 'A9',
    or 'B1' to B9', respectively.

    If the index is alphanumeric, in the range 'AA' to 'AY',
    or 'BA' to 'BY', it returns an index in the range 'AB' to 'AZ',
    or 'BB' to 'BZ, respectively.

    It raises exceptions if it is not an index or the index is increased
    beyond the allowed ranges.

    Parameters
    ----------
    idx : str
        The index to be increased by one unit.

    Returns
    -------
    : str
        The index increased by one unit.

    Raises
    ------
    Exception if string is not an index.

    Exception if numeric index increases beyond 99.

    Exception if alphanumeric index increases beyond A9 or B9.

    Exception if alphanumeric index increases beyond AZ or BZ.
    """
    if not is_index(idx):
        raise Exception('String is not an index')

    if idx.isdecimal():
        n = int(idx) + 1
        if n > 99:
            raise Exception('Increasing numeric index beyond 99')
        idx_plus_one = str(n).zfill(2)
    else:
        if idx[1] == 9:
            raise Exception('Increasing alphanumeric index beyond A9 or B9')
        if idx[1] == 'Z':
            raise Exception('Increasing alphanumeric index beyond AZ or BZ')
        idx_plus_one = idx[0] + chr(ord(idx[1])+1)
    return idx_plus_one


def is_marker_cell(marker: str = None,
                   cell: nbformat.notebooknode.NotebookNode = None) -> bool:
    """Checks whether the given `cell` starts with the given `marker`.

    Parameters
    ----------
    marker : str
        The marker to be searched for.

    cell : nbformat.notebooknode.NotebookNode
        The cell to be checked.

    Returns
    -------
    : bool
        True or False, depending on whether the cell starts with the
        marker or not.
    """
    return cell.source.startswith(marker)


def refresh_marker_cells(path_to_notes: str = '.', marker: str = None,
                         mode: str = 'remove') -> None:
    """Removes or cleans the contents of any cell with the given `marker`
    from the indexed notebooks in path_to_notes.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    marker : str
        The marker to be searched for.

    mode : str
        A string indicating whether to clean (if mode == 'clean')
        or remove (if mode == 'remove') the cells marked with the
        provided `marker`. The mode 'clean' leaves the MAKER in the cell,
        but no other content in the source. The useful thing about the
        'clean' mode is to preserve any metadata that differs from the
        default ones added by the binder (such as about the slide property).
    """
    if marker and mode in ('clean', 'remove'):
        for nb_name in indexed_notebooks(path_to_notes):
            nb_file = os.path.join(path_to_notes, nb_name)
            nb = nbformat.read(nb_file, as_version=4)

            new_cells = []
            for cell in nb.cells:
                if not is_marker_cell(marker, cell):
                    new_cells.append(cell)
                elif mode == 'clean':
                    logging.info("- cleaning '{arg1}' cell from {arg2}",
                                 arg1=marker, arg2=nb_name)
                    new_cells.append(cell)
                    new_cells[-1].source = marker
                elif mode == 'remove':
                    logging.info("- cleaning '{arg1}' cell from {arg2}",
                                 arg1=marker, arg2=nb_name)

            nb.cells = new_cells
            nbformat.write(nb, nb_file)


def get_nb_title(path_to_notes: str = '.', nb_name: str = None) -> str:
    """Returns the title of a juyter notebook.

    It looks for the first cell, in the notebook, that starts with
    a single markdown symbol '#' and returns the contents of the first
    line of this cell, striped out of '# ' and the remaining lines.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    nb_name : str
        The name of the jupyter notebook file.

    Returns
    -------
    : str
        The desired title of the notebook or "" if not found.
    """
    nb = nbformat.read(os.path.join(path_to_notes, nb_name), as_version=4)
    for cell in nb.cells:
        if cell.source.startswith('#'):
            return cell.source[1:].splitlines()[0].strip()
    return None


def get_nb_full_entry(path_to_notes: str = '.',
                      nb_name: str = None) -> list:
    """Returns the full entry of a notebook.

    This entry is to be used for the link to the notebook from the
    table of contents and from the navigators.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    nb_name : str
        The name of the jupyter notebook file.

    Returns
    -------
    markdown_entry : str
        The type of markdown header or identation for the entry in
        Table of Contents

    notebook_entry : str
        The full notebook entry, with the title, preceeded,
        depending on the case, of the Chapter and Section numbers
        or letters.
    """
    chapter, section = REG.match(nb_name).group(1, 2)

    if chapter.isdecimal():
        chapter_clean = int(chapter)
    else:
        chapter_clean = chapter[1]
    title = get_nb_title(path_to_notes, nb_name)

    if chapter == '00' or chapter[0] == 'B' or section == '':
        markdown_entry = '### '
        num_entry = ''
    elif section == '00':
        markdown_entry = '### '
        num_entry = '{}. '.format(chapter_clean)
    else:
        markdown_entry = '&nbsp;&nbsp;&nbsp;&nbsp; '
        num_entry = '{}.{}. '.format(chapter_clean, int(section))

    return markdown_entry, num_entry, title


def get_nb_entry(path_to_notes: str = '.',
                 nb_name: str = None,
                 show_index: bool = True) -> str:
    """Returns the entry of a notebook.

    This entry is to be used for the link to the notebook from the
    table of contents and from the navigators. Depending on the
    value of the argument `show_index`, the entry can be either
    the full entry provided by the function `get_nb_full_entry()`
    or simply the title of the notebook, provided by the function
    `get_nb_title()`.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    nb_name : str
        The name of the jupyter notebook file.

    show_index : boolean
        Indicates whether to include the chapter and section numbers
        of the notebook in the table of contents (if True) or just
        the title (if False).

    Returns
    -------
    entry : str
        A string with the entry name.
    """
    if show_index:
        entry = ''.join(list(get_nb_full_entry(path_to_notes, nb_name)[1:3]))
    else:
        entry = get_nb_title(path_to_notes, nb_name)
    return entry


def yield_contents(path_to_notes: str = '.',
                   show_index_in_toc: bool = True) -> Iterable[str]:
    """Iterable with entries for each of the indexed notebooks.

    It takes all the indexed notebooks and it creates a generator
    function to iterate from one notebook to the next, returning,
    each time, the navigator entry associated with that notebook.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    show_index_in_toc : bool
        Whether to display the navigator with the chapter
        and section number of each notebook or just their title.

    Yields
    ------
    : Iterable[str]
        Next navigator entry in the iterator
    """
    for nb_name in indexed_notebooks(path_to_notes):
        markdown_entry, num_entry, title \
            = get_nb_full_entry(path_to_notes, nb_name)
        if show_index_in_toc:
            yield '{}[{}]({})\n'.format(markdown_entry,
                                        num_entry + title,
                                        nb_name)
        else:
            yield '{}[{}]({})\n'.format(markdown_entry, title, nb_name)


def get_contents(path_to_notes: str = '.',
                 toc_title: str = '',
                 show_index_in_toc: bool = True) -> str:
    """Returns the 'Table of Contents'.

    Returns a string with the 'Table of Contents' constructed
    from the collection of notebooks in the folder indicated by
    the argument `path_to_notes`.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    toc_title : str
        Text to be displayed as the title for the table of contents cell,
        e.g. 'Contents', 'Table of Contents', or in other languages,
        'Conteúdo', 'Table des Matières', and so on.

    show_index_in_toc : bool
        Whether to display the table of contents with the chapter
        and section number of each notebook or just their title.

    Returns
    -------
    : str
        The table of contents.
    """

    contents = TOC_MARKER + "\n## [" + toc_title + "](#)\n\n"
    for item in yield_contents(path_to_notes, show_index_in_toc):
        contents += item + "\n"

    return contents


def insert_notebooks(path_to_notes: str = '.') -> None:
    """Includes a notebook in the colllection.

    Checks whether there is any notebook that matches the regular expression
    indicating it is to be incuded in the collection of indexed notebooks
    and, if so, renames the affected notebooks in the appropriate order.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.
    """

    nb_names_ins = sorted(nb for nb in os.listdir(path_to_notes)
                          if REG_INSERT.match(nb))
    nb_names_new = nb_names_ins.copy()

    for j in range(len(nb_names_ins)):
        nbj_reg = REG_INSERT.match(nb_names_new[j])
        if nbj_reg.group(4):
            for k in range(j, len(nb_names_ins)):
                nbk_reg = REG_INSERT.match(nb_names_new[k])
                if nbk_reg.group(1, 2) == nbj_reg.group(1, 2):
                    gk3 = nbk_reg.group(3)
                    if nbk_reg.group(1, 2, 3, 4) == nbj_reg.group(1, 2, 3, 4):
                        gk3_new = increase_index(gk3)
                        gk4_new = ''
                    else:
                        gk3_new = increase_index(gk3)
                        gk4_new = nbk_reg.group(4)
                    nb_names_new[k] = nbk_reg.group(1) + nbk_reg.group(2) \
                        + '.' + gk3_new + gk4_new + '-' + nbk_reg.group(5) \
                        + nbk_reg.group(6)
        if nbj_reg.group(2):
            nb_names_new[j] = nb_names_new[j][:nbj_reg.start(2)] \
                + nb_names_new[j][nbj_reg.end(2):]
            for k in range(j, len(nb_names_ins)):
                nbk_reg = REG_INSERT.match(nb_names_new[k])
                if nbk_reg.group(1)[0] == nbj_reg.group(1)[0]:
                    gk1_new = increase_index(nbk_reg.group(1))
                    if nbk_reg.group(1, 2) == nbj_reg.group(1, 2):
                        gk2_new = ''
                    else:
                        gk2_new = nbk_reg.group(2)
                    nb_names_new[k] = gk1_new + gk2_new + '.' \
                        + nbk_reg.group(3) + nbk_reg.group(4) + '-' \
                        + nbk_reg.group(5) + nbk_reg.group(6)

    if nb_names_new == nb_names_ins:
        logging.info('- no files need renaming, no reindexing needed')
    else:
        count = 0
        for f, f_new in zip(nb_names_ins, nb_names_new):
            count += 1
            if f != f_new:
                logging.info('- replacing {arg1} with {arg2}',
                             arg1=f, arg2=f_new)
            os.rename(os.path.join(path_to_notes, f),
                      os.path.join(path_to_notes, str(count) + '-' + f_new))
        count = 0
        for f_new in nb_names_new:
            count += 1
            os.rename(os.path.join(path_to_notes, str(count) + '-' + f_new),
                      os.path.join(path_to_notes, f_new))


def tighten_notebooks(path_to_notes: str = '.') -> None:
    """Tighten the indexes of the notebooks in the colllection.

    Checks whether there are gaps in the indices of the notebooks
    and, if so, renames the affected notebooks in the appropriate
    order.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.
    """

    nb_names = sorted(nb for nb in os.listdir(path_to_notes) if REG.match(nb))
    nb_names_new = nb_names.copy()

    nb_reg = [REG.match(nb_names) for nb_names in nb_names]
    nb_new_reg = nb_reg.copy()

    for j in range(len(nb_names)):
        if j == 0:
            if (nb_reg[j].group(1).isdecimal()
                    and nb_reg[j].group(1) >= '02'):
                nb_names_new[j] = '01.' + nb_reg[j].group(2) \
                    + '-' + ''.join(nb_reg[j].group(3, 4))
            elif (nb_reg[j].group(1).isalpha()
                  and nb_reg[j].group(1)[1] >= 'B'):
                nb_names_new[j] = nb_reg[j].group(1)[0] \
                    + 'A.' + nb_reg[j].group(2) \
                    + '-' + ''.join(nb_reg[j].group(3, 4))
            elif (nb_reg[j].group(1).isalnum()
                  and nb_reg[j].group(1)[1] >= '2'):
                nb_names_new[j] = nb_reg[j].group(1)[0] \
                    + '1.' + nb_reg[j].group(2) \
                    + '-' + ''.join(nb_reg[j].group(3, 4))
        else:
            if (nb_reg[j].group(1).isdecimal()
                    and nb_reg[j].group(1) >= '02'):
                if nb_reg[j].group(1) == nb_reg[j-1].group(1):
                    nb_names_new[j] = nb_new_reg[j-1].group(1) \
                        + '.' + nb_reg[j].group(2) \
                        + '-' + ''.join(nb_reg[j].group(3, 4))
                elif (nb_reg[j].group(1)
                      > increase_index(nb_new_reg[j-1].group(1))):
                    nb_names_new[j] = \
                        increase_index(nb_new_reg[j-1].group(1)) \
                        + '.' + nb_reg[j].group(2) \
                        + '-' + ''.join(nb_reg[j].group(3, 4))
            elif (nb_reg[j].group(1)[0] in ('A', 'B')
                  and nb_reg[j].group(1)[1] >= 'B'):
                if (nb_reg[j].group(1)[0] == 'A'
                        and nb_new_reg[j-1].group(1).isdecimal()):
                    nb_names_new[j] = 'AA.' + nb_reg[j].group(2) \
                        + '-' + ''.join(nb_reg[j].group(3, 4))
                elif (nb_reg[j].group(1)[0] == 'B'
                      and nb_new_reg[j-1].group(1)[0] == 'A'):
                    nb_names_new[j] = 'BA.' + nb_reg[j].group(2) \
                        + '-' + ''.join(nb_reg[j].group(3, 4))
                elif nb_reg[j].group(1) == nb_reg[j-1].group(1):
                    nb_names_new[j] = nb_new_reg[j-1].group(1) \
                        + '.' + nb_reg[j].group(2) \
                        + '-' + ''.join(nb_reg[j].group(3, 4))
                elif (nb_reg[j].group(1)
                      > increase_index(nb_new_reg[j-1].group(1))):
                    nb_names_new[j] = \
                        increase_index(nb_new_reg[j-1].group(1)) \
                        + '.' + nb_reg[j].group(2) \
                        + '-' + ''.join(nb_reg[j].group(3, 4))
        nb_new_reg[j] = REG.match(nb_names_new[j])

    nb_names_newest = nb_names_new.copy()

    nb_new_reg = [REG.match(nb_name_new) for nb_name_new in nb_names_new]
    nb_newest_reg = nb_new_reg.copy()

    for j in range(len(nb_names_new)):
        if j == 0 or nb_new_reg[j].group(1) != nb_new_reg[j-1].group(1):
            if (nb_new_reg[j].group(2).isdecimal()
                    and nb_new_reg[j].group(2) >= '02'):
                nb_names_newest[j] = nb_new_reg[j].group(1) \
                    + '.01-' + ''.join(nb_new_reg[j].group(3, 4))
            elif (nb_new_reg[j].group(2)[0] == 'A'
                  and nb_new_reg[j].group(2)[1] >= 'B'):
                nb_names_newest[j] = nb_new_reg[j].group(1) \
                    + '.AA-' + ''.join(nb_new_reg[j].group(3, 4))
            elif (nb_new_reg[j].group(2) == 'B'
                  and nb_new_reg[j].group(2)[1] >= 'B'):
                nb_names_newest[j] = nb_new_reg[j].group(1) \
                    + '.BA-' + ''.join(nb_new_reg[j].group(3, 4))
        else:
            if (nb_new_reg[j].group(2).isdecimal()
                    and nb_new_reg[j].group(2)
                    > increase_index(nb_newest_reg[j-1].group(2))):
                nb_names_newest[j] = nb_new_reg[j].group(1) + '.' \
                    + increase_index(nb_newest_reg[j-1].group(2)) \
                    + '-' + ''.join(nb_new_reg[j].group(3, 4))
            elif (nb_new_reg[j].group(2)[0] in ('A', 'B')
                  and nb_new_reg[j].group(2)[1] >= 'B'):
                if (nb_new_reg[j].group(2)[0] == 'A'
                        and nb_newest_reg[j-1].group(2).isdecimal()):
                    nb_names_newest[j] = nb_new_reg[j].group(1) \
                        + '.AA-' + ''.join(nb_new_reg[j].group(3, 4))
                elif (nb_new_reg[j].group(2)[0] == 'B'
                      and nb_newest_reg[j-1].group(1)[0] != 'B'):
                    nb_names_newest[j] = nb_new_reg[j].group(1) \
                        + '.BA-' + ''.join(nb_new_reg[j].group(3, 4))
                elif (nb_new_reg[j].group(2)
                      > increase_index(nb_newest_reg[j-1].group(2))):
                    nb_names_newest[j] = nb_new_reg[j].group(1) + '.' \
                        + increase_index(nb_newest_reg[j-1].group(2)) \
                        + '-' + ''.join(nb_new_reg[j].group(3, 4))
        nb_newest_reg[j] = REG.match(nb_names_newest[j])

    if nb_names_newest == nb_names:
        logging.info('- no files need renaming, no reindexing needed')
    else:
        count = 0
        for f, f_newest in zip(nb_names, nb_names_newest):
            count += 1
            if f != f_newest:
                logging.info('- replacing {arg1} with {arg2}',
                             arg1=f, arg2=f_newest)
            os.rename(os.path.join(path_to_notes, f),
                      os.path.join(path_to_notes, str(count) + '-' + f_newest))
        count = 0
        for f_newest in nb_names_newest:
            count += 1
            os.rename(os.path.join(path_to_notes, str(count) + '-' + f_newest),
                      os.path.join(path_to_notes, f_newest))


def reindex(path_to_notes: str = '.',
            insert: bool = True,
            tighten: bool = False) -> None:
    """Reindex the collection of notebooks.

    Reindex the notebooks by inserting (by calling `insert_notebooks`)
    and/or tightening (by calling `tighten_notebooks`) the collection
    of notebooks, depending on whether the arguments `insert` and/or
    `tighten` are True or False.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    insert : bool
        Whether to insert notebooks in the collection or not.

    tighten : bool
        Whether to tighten the indices of notebooks or not.
    """
    if insert:
        insert_notebooks(path_to_notes)

    if tighten:
        tighten_notebooks(path_to_notes)


def export_notebooks(path_to_notes: str = '.',
                     export_path: str = None,
                     exporter_name: str = None,
                     exporter_args: dict = None) -> None:
    """
    Export notebooks via nbconvert.

    It reads all the notes in `path_to_notes` and export them to
    the directory `export_path` using the exporter defined by
    `exporter_name`, with the arguments in `exporter_args`.

    The name of the exporter (`exporter_name`) must be one of the default
    exporters listed in `nbconvert.exporters.get_export_names()`.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    export_path : str
        The path to the directory where the exported, or converted,
        files should be saved in.

    exporter_name : str
        The name of the exporter to be used in `nbconvert` via
        `nbconvert.exporters.get_exporter(exporter_name)`. Possible
        choices are 'markdown', 'pdf', 'slides', 'latex', etc.

    exporter_args : dict
        Arguments to be passed on to the exporter via
        `nbconvert.exporters.get_exporter(exporter_name)(**exporter_args)`.
    """
    assert(isinstance(export_path, str)), "Argument `export_path` should \
        be a string"
    assert(exporter_name in exporters.get_export_names()), "The \
        `exporter_name` argument with value {} is not in the \
        list of available exporters listed in \
        `nbconvert.exporters.get_export_names()`".format(exporter_name)

    if os.path.isdir(export_path):
        for f in os.listdir(export_path):
            os.remove(os.path.join(export_path, f))
    else:
        os.mkdir(export_path)

    if exporter_args:
        exporter = exporters.get_exporter(exporter_name)(**exporter_args)
    else:
        exporter = exporters.get_exporter(exporter_name)()
    extension = exporter.file_extension

    for nb_name in indexed_notebooks(path_to_notes):
        nb_file = os.path.join(path_to_notes, nb_name)
        nb = nbformat.read(nb_file, as_version=4)
        body = exporter.from_notebook_node(nb)[0]
        for cell in nb.cells:
            for marker in (NAVIGATOR_MARKER, TOC_MARKER):
                if is_marker_cell(marker, cell):
                    source_new = ''
                    i = 0
                    for m in REG_LINK.finditer(cell.source):
                        source_new += cell.source[i:m.start(5)] + extension
                        i = m.end(5)
                    source_new += cell.source[i:]
                    cell.source = source_new

        logging.info("Adjusting links for {arg}", arg=export_path)
        body = exporter.from_notebook_node(nb)[0]
        export_filename = \
            os.path.join(export_path,
                         nb_name[:REG.match(nb_name).start(4)]
                         + extension)
        if isinstance(body, str):
            export_file = open(export_filename, 'w+')
        else:
            export_file = open(export_filename, 'wb+')
        export_file.write(body)
        export_file.close()


def add_contents(path_to_notes: str = '.',
                 toc_nb_name: str = None,
                 toc_title: str = '',
                 show_index_in_toc: bool = True) -> None:
    """Adds the table of contents to a selected notebook.

    It adds the table of contents, generated from the collection of
    notebooks in the directory `path_to_notes`, to the notebook
    `toc_nb_name`, with `toc_title` as the title of the Table
    of Contents. The inclusion, or not, of the Chapter and Section
    numbers in the table of contents is indicaded by the argument
    `show_index_in_toc`.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    toc_nb_name : str
        filename of the notebook in which the table of contents
        is to be inserted

    toc_title : str
        Text to be displayed as the title for the table of contents cell,
        e.g. 'Contents', 'Table of Contents', or in other languages,
        'Conteúdo', 'Table des Matières', and so on.

    show_index_in_toc : bool
        Whether to display the navigator with the chapter
        and section number of each notebook or just their title.
    """
    # error handling
    assert(isinstance(path_to_notes, str)), "Argument `path_to_notes` \
        should be a string"
    assert(isinstance(toc_nb_name, str)), "Argument `toc_nb_name` \
        should be a string"
    assert(isinstance(toc_title, str)), "Argument `toc_title` \
        should be a string"

    contents = get_contents(path_to_notes, toc_title, show_index_in_toc)

    toc_nb_file = os.path.join(path_to_notes, toc_nb_name)

    toc_nb = nbformat.read(toc_nb_file, as_version=4)

    toc_cell_found = False
    for cell in toc_nb.cells:
        if is_marker_cell(TOC_MARKER, cell):
            cell.source = contents
            cell.metadata = SLIDE_SHOW
            toc_cell_found = True

    if toc_cell_found:
        nbformat.write(toc_nb, toc_nb_file)
        logging.info('- Table of contents updated in {arg}', arg=toc_nb_name)
    else:
        logging.info('* No markdown cell starting with {arg1} found in {arg2}',
                     arg1=TOC_MARKER, arg2=toc_nb_name)
        logging.info("- inserting table of contents in {arg}",
                     arg=toc_nb_name)
        if toc_nb.cells and is_marker_cell(NAVIGATOR_MARKER, toc_nb.cells[-1]):
            toc_nb.cells.insert(-1, new_markdown_cell(source=contents,
                                                      metadata=SLIDE_SHOW))
        else:
            toc_nb.cells.append(new_markdown_cell(source=contents,
                                                  metadata=SLIDE_SHOW))

    nbformat.write(toc_nb, toc_nb_file)


def add_headers(path_to_notes: str = '.', header: str = None) -> None:
    """Adds header to each notebook in the collection.

    It adds the provided `header`as the first cell of each notebook
    in the collection of indexed notebooks in the folder `path_to_notes`.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    header : str
        The string with the contents to be included in the header cell.
    """
    for nb_name in indexed_notebooks(path_to_notes):
        nb_file = os.path.join(path_to_notes, nb_name)
        nb = nbformat.read(nb_file, as_version=4)

        if nb.cells and is_marker_cell(HEADER_MARKER, nb.cells[0]):
            logging.info('- updating header for {arg}', arg=nb_name)
            nb.cells[0].source = HEADER_MARKER + '\n' + header
            nb.cells[0].metadata = SLIDE_SKIP
        else:
            logging.info('- inserting header for {arg}', arg=nb_name)
            nb.cells.insert(0, new_markdown_cell(
                source=HEADER_MARKER + '\n' + header,
                metadata=SLIDE_SKIP))
        nbformat.write(nb, nb_file)


def get_badge_entries(path_to_notes: str = '.',
                      user: str = '',
                      repository: str = '',
                      branch: str = 'master',
                      github_nb_dir: str = '.',
                      custom_badges: list = None) -> Iterable[tuple]:
    """Iterable with the bagdes info for each notebook.

    It reads the indexed notebooks in the folder `path_to_notes` and
    generates an iterable with the information needed to build the
    badges for each notebook.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    user : str
        The github username of the onwer of the repository in which
        the notebooks reside, in case one wants to add a badge to
        open up the notebooks in one of the configured cloud
        computing platforms (google colab and binder).

    repository : str
        The name of the github repository mentioned in the description
        of the `user` argument.

    branch : str
        The name of the branch of the github repository mentioned in
        the description of the `user` argument.

    github_nb_dir : str
        The path to the notebooks, from the root directory of the
        repository mentioned in the description of the `user` argument.

    custom_badges : list of dict
        A list of dictionaries with the necessary information
        to add custom badges.

        Each dictionary in the list should have the following keys:
        `name` (str), `title` (str), `url` (str), `replace_links` (bool),
        `extension` (str), `label` (str), `message` (str), and
        `color` (str).

        The keys `name`, `title` and `url` are used for the building
        the `href` link in the badge, with `name` being the `alt`
        argument of `href`.

        The keys `replace_links` and `extension` are used to replace
        the `.ipynb` extension of each notebook to the appropriate
        extension, e.g `.md`, `.slides.html`, `.pdf`, `.py`, `.tex`,
        and so on.

        The keys `label`, `message`, and `color` are used to build
        the badge via the `shields.io` constructor.

    Yields
    ------
    : str
        Path to current notebook in the iterator.
    : str
        The google colab link for the current notebook in the iterator.
    : str
        The binder link for the current notebook in the iterator.
    : list
        The list of extra badge links for the current notebook
        in the iterator.
    """

    for this_nb in indexed_notebooks(path_to_notes):
        this_nb_colab_link \
            = COLAB_LINK.format(user=user,
                                repository=repository,
                                branch=branch,
                                github_nb_dir=github_nb_dir,
                                notebook_filename=os.path.basename(this_nb))

        this_nb_binder_link \
            = BINDER_LINK.format(user=user,
                                 repository=repository,
                                 branch=branch,
                                 github_nb_dir=github_nb_dir,
                                 notebook_filename=os.path.basename(this_nb))

        this_nb_custom_badge_links = []

        if custom_badges:
            for badge in custom_badges:
                this_nb_custom_badge_links.append(CUSTOM_BADGE_LINK.format(
                    badge_url=badge['url'],
                    badge_filename=this_nb[:REG.match(this_nb).start(4)]
                    + badge['extension'],
                    badge_label=badge['label'],
                    badge_message=badge['message'],
                    badge_color=badge['color'],
                    badge_alt=badge['name'],
                    badge_title=badge['title']))

        yield os.path.join(path_to_notes, this_nb), \
            this_nb_colab_link, this_nb_binder_link, \
            this_nb_custom_badge_links


def add_badges(path_to_notes: str = '.',
               user: str = '',
               repository: str = '',
               branch: str = 'master',
               github_nb_dir: str = '.',
               custom_badges: list = None,
               show_colab: bool = False,
               show_binder: bool = False) -> None:
    """Adds badges to each notebook in the collection.

    Adds top and bottom badges to each notebook in the collection
    of indexed notebooks in the folder `path_to_notes`.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    user : str
        The github username of the onwer of the repository in which
        the notebooks reside, in case one wants to add a badge to
        open up the notebooks in one of the configured cloud
        computing platforms (google colab and binder).

    repository : str
        The name of the github repository mentioned in the description
        of the `user` argument.

    branch : str
        The name of the branch of the github repository mentioned in
        the description of the `user` argument.

    github_nb_dir : str
        The path to the notebooks, from the root directory of the
        repository mentioned in the description of the `user` argument.

    custom_badges: list of dict
        Info for building extra badges. See the docstring
        of `get_badge_entries()`

    show_colab : bool
        Whether to display the Google Colab badge or not.

    show_binder : bool
        Whether to display the Binder badge or not.
    """
    for nb_filename, \
        this_nb_colab_link, \
        this_nb_binder_link, \
        this_nb_custom_badge_links \
            in get_badge_entries(path_to_notes,
                                 user,
                                 repository,
                                 branch,
                                 github_nb_dir,
                                 custom_badges):
        nb = nbformat.read(nb_filename, as_version=4)
        nb_name = os.path.basename(nb_filename)

        badges_top = BADGES_MARKER + "\n"

        if show_colab:
            badges_top += this_nb_colab_link + "&nbsp;"

        if show_binder:
            badges_top += this_nb_binder_link + "&nbsp;"

        for this_nb_custom_badge_link in this_nb_custom_badge_links:
            badges_top += this_nb_custom_badge_link + "&nbsp;"

        if len(nb.cells) > 1 and is_marker_cell(BADGES_MARKER, nb.cells[1]):
            logging.info("- updating badges for {arg}", arg=nb_name)
            nb.cells[1].source = badges_top
            nb.cells[1].metadata = SLIDE_SKIP
        else:
            logging.info("- inserting badges for {arg}", arg=nb_name)
            nb.cells.insert(1, new_markdown_cell(source=badges_top,
                                                 metadata=SLIDE_SKIP))

        nbformat.write(nb, nb_filename)


def prev_this_next(collection: list = None) -> None:
    """Iterable with previous, current, and next notebooks in `collection`.

    It reads a list of indexed notebooks and gives an iterable with the
    previous, current, and next notebooks for each notebook in the list.

    Parameters
    ----------
    collection : list of str
        The collection of indexed notebooks.

    Yields
    ------
    : str
        A string with the filename of the previous notebook in the iteration.
    : str
        A string with the filename of the current notebook in the iteration.
    : str
        A string with the filename of the next notebook in the iteration.
    """
    a, b, c = itertools.tee(collection, 3)
    next(c)
    return zip(itertools.chain([None], a), b, itertools.chain(c, [None]))


def get_navigator_entries(path_to_notes: str = '.',
                          core_navigators: list = None,
                          show_nb_title_in_nav: bool = True,
                          show_index_in_nav: bool = True) -> Iterable[str]:
    """Iterable with the navigator info for each notebook.

    It reads the indexed notebooks in the folder `path_to_notes` and
    generates an iterable with the information needed to build the
    navigators for each notebook.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    core_navigators : list of str
        A lists of strings with the filenames of each notebook to be
        included in the navigators, in between the links to the
        "previous" and the "next" notebooks.

    show_nb_title_in_nav : bool
        Whether to diplay the title of the notebook in the previous
        and next links or just display the words 'Previous' and 'Next'.

    show_index_in_nav : bool
        Whether to display the navigator with the chapter
        and section number of each notebook or just their title.

    Yields
    ------
    : str
        Path to current notebook in the iterator.
    : str
        Contents of the navigation bar for the current notebook in the
        iterator.
    """
    for prev_nb, this_nb, next_nb \
            in prev_this_next(indexed_notebooks(path_to_notes)):
        navbar = ""
        if prev_nb:
            if show_nb_title_in_nav:
                entry = get_nb_entry(path_to_notes, prev_nb,
                                     show_index_in_nav)
                navbar += PREV_TEMPLATE.format(title=entry, url=prev_nb)
            else:
                navbar += PREV_TEMPLATE.format(title='Previous', url=prev_nb)

        for center_nb in core_navigators:
            entry = get_nb_entry(path_to_notes, center_nb,
                                 show_index_in_nav)
            navbar += CENTER_TEMPLATE.format(title=entry, url=center_nb)

        if next_nb:
            if show_nb_title_in_nav:
                entry = get_nb_entry(path_to_notes, next_nb,
                                     show_index_in_nav)
                navbar += NEXT_TEMPLATE.format(title=entry, url=next_nb)
            else:
                navbar += NEXT_TEMPLATE.format(title='Next', url=next_nb)

        yield os.path.join(path_to_notes, this_nb), navbar


def add_navigators(path_to_notes: str = '.',
                   core_navigators: list = None,
                   show_nb_title_in_nav: bool = True,
                   show_index_in_nav: bool = True) -> None:
    """Adds navigators to each notebook in the collection.

    Adds top and bottom navigators to each notebook in the collection
    of indexed notebooks in the folder `path_to_notes`.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    core_navigators : list of str
        A lists of strings with the filenames of each notebook to be
        included in the navigators, in between the links to the
        "previous" and the "next" notebooks.

    show_nb_title_in_nav : bool
        Whether to diplay the title of the notebook in the previous
        and next links or just display the words 'Previous' and 'Next'.

    show_index_in_nav : bool
        Whether to display the navigator with the chapter
        and section number of each notebook or just their title.
    """
    for nb_file, navbar \
        in get_navigator_entries(path_to_notes,
                                 core_navigators,
                                 show_nb_title_in_nav,
                                 show_index_in_nav):
        nb = nbformat.read(nb_file, as_version=4)
        nb_name = os.path.basename(nb_file)

        navbar_top = NAVIGATOR_MARKER + "\n" + navbar + "\n\n---\n"
        navbar_bottom = NAVIGATOR_MARKER + "\n\n---\n" + navbar

        if len(nb.cells) >= 1 and is_marker_cell(NAVIGATOR_MARKER,
                                                 nb.cells[1]):
            logging.info("- updating navbar for {arg}", arg=nb_name)
            nb.cells[1].source = navbar_top
            nb.cells[1].metadata = SLIDE_SKIP
        elif len(nb.cells) >= 2 and is_marker_cell(NAVIGATOR_MARKER,
                                                   nb.cells[2]):
            logging.info("- updating navbar for {arg}", arg=nb_name)
            nb.cells[2].source = navbar_top
            nb.cells[2].metadata = SLIDE_SKIP
        else:
            logging.info("- inserting navbar for {arg}", arg=nb_name)
            nb.cells.insert(1, new_markdown_cell(source=navbar_top,
                                                 metadata=SLIDE_SKIP))

        if len(nb.cells) > 2 and is_marker_cell(NAVIGATOR_MARKER,
                                                nb.cells[-1]):
            nb.cells[-1].source = navbar_bottom
            nb.cells[-1].metadata = SLIDE_SHOW
        else:
            nb.cells.append(new_markdown_cell(source=navbar_bottom,
                                              metadata=SLIDE_SHOW))
        nbformat.write(nb, nb_file)


def bind_from_arguments(path_to_notes: str = '.',
                        insert: bool = False,
                        tighten: bool = False,
                        toc_nb_name: str = '',
                        toc_title: str = '',
                        header: str = '',
                        core_navigators: list = None,
                        user: str = '',
                        repository: str = '',
                        branch: str = 'master',
                        github_nb_dir: str = '.',
                        custom_badges: list = None,
                        show_colab: bool = False,
                        show_binder: bool = False,
                        show_index_in_toc: bool = True,
                        show_nb_title_in_nav: bool = True,
                        show_index_in_nav: bool = True) -> None:
    """Binds the collection of notebooks from the arguments provided.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks,
        either the absolute path or the path relative from
        where the code is being ran.

    insert : bool
        Indicates whether to insert notebooks in the collection of
        indexed notebooks or not.

    tighten : bool
        Indicates whether to tighten the indices of the notebooks,
        i.e. whether there are gaps in the indices of the notebooks
        and, if so, rename the affected notebooks in the
        appropriate order.

    toc_nb_name : str
        Filename of the notebook in which the table of contents
        is to be inserted

    toc_title : str
        Text to be displayed as the title for the table of contents cell,
        e.g. 'Contents', 'Table of Contents', or in other languages,
        'Conteúdo', 'Table des Matières', and so on.

    header : str
        The string with the contents to be included in the header cell.

    core_navigators : list of str
        A lists of strings with the filenames of each notebook to be
        included in the navigators, in between the links to the
        "previous" and the "next" notebooks.

    user : str
        The github username of the onwer of the repository in which
        the notebooks reside, in case one wants to add a badge to
        open up the notebooks in one of the configured cloud
        computing platforms (google colab and binder).

    repository : str
        The name of the github repository mentioned in the description
        of the `user` argument.

    branch : str
        The name of the branch of the github repository mentioned in
        the description of the `user` argument.

    github_nb_dir : str
        The path to the notebooks, from the root directory of the
        repository mentioned in the description of the `user` argument.

    show_colab : bool
        Whether to display the Google Colab badge or not.

    show_binder : bool
        Whether to display the Binder badge or not.

    show_index_in_toc : bool
        Whether to display the navigator with the chapter
        and section number of each notebook or just their title.

    show_nb_title_in_nav : bool
        Whether to diplay the title of the notebook in the previous
        and next links or just display the words 'Previous' and 'Next'.

    show_index_in_nav : bool
        Whether to display the navigator with the chapter
        and section number of each notebook or just their title.
    """

    if insert or tighten:
        reindex(path_to_notes, insert, tighten)

    refresh_marker_cells(path_to_notes, HEADER_MARKER, 'remove')
    refresh_marker_cells(path_to_notes, NAVIGATOR_MARKER, 'remove')

    add_contents(path_to_notes=path_to_notes,
                 toc_nb_name=toc_nb_name,
                 toc_title=toc_title,
                 show_index_in_toc=show_index_in_toc)

    add_headers(path_to_notes=path_to_notes, header=header)

    add_navigators(path_to_notes=path_to_notes,
                   core_navigators=core_navigators,
                   show_nb_title_in_nav=show_nb_title_in_nav,
                   show_index_in_nav=show_index_in_nav)

    add_badges(path_to_notes=path_to_notes,
               user=user,
               repository=repository,
               branch=branch,
               github_nb_dir=github_nb_dir,
               custom_badges=custom_badges,
               show_colab=show_colab,
               show_binder=show_binder)


def bind_from_configfile(config_file: str) -> None:
    """Binds the collection of notebooks from a configuration file.

    It reads the given configuration file in YAML format and pass
    the arguments in the configuration file to the function
    `bind_from_arguments()`.

    Parameters
    ----------
    config_file : str
        The filename of the configuration file.
    """
    with open(config_file, 'r') as cf:
        config = yaml.load(cf, Loader=yaml.FullLoader)

    if 'path_to_notes' in config:
        path_to_notes = config['path_to_notes']
    else:
        path_to_notes = '.'

    if 'reindexing' in config:
        reindex(path_to_notes, **config['reindexing'])

    key_marker = {
        'header': HEADER_MARKER,
        'navigatores': NAVIGATOR_MARKER,
        'badges': BADGES_MARKER
    }
    for key in key_marker:
        if key in config:
            mode = 'clean'
        else:
            mode = 'remove'
        refresh_marker_cells(path_to_notes, key_marker[key], mode)

    if 'contents' in config:
        add_contents(path_to_notes=path_to_notes, **config['contents'])

    if 'header' in config:
        add_headers(path_to_notes=path_to_notes, header=config['header'])

    if 'navigators' in config:
        add_navigators(path_to_notes=path_to_notes, **config['navigators'])

    if 'badges' in config:
        add_badges(path_to_notes=path_to_notes, **config['badges'])

    if 'exports' in config:
        for export in config['exports']:
            export_notebooks(path_to_notes=path_to_notes, **export)


def bind(*args, **kargs) -> None:
    """Binds the collection of notebooks.

    It expects either a configuration file or a list of arguments in
    order to bind the collection of indexed notebooks.

    If the first argument is a string ending with either '.yml' or
    '.yaml', it assumes this is the filename of a configuration file
    and pass it on to the function `bind_from_configfile()`.

    Otherwise, it assumes it is given directly the arguments to bind
    the collections and pass them on to the function
    `bind_from_arguments()`.

    Parameters
    ----------
    *args : Variable arguments used to check whether a configuration file
        or path_to_notes is given
    *kargs: Variable keyword arguments to be passed to function
        `bind_from_arguments()` in case a configuration file is not given

    See also
    --------
    bind_from_arguments : binds the notebooks from the arguments provided.

    bind_from_configfile: binds the notebooks using a configuration file.
    """
    if args and args[0].endswith(('.yml', '.yaml')):
        bind_from_configfile(args[0])
    elif 'path_to_notes' in kargs.keys():
        bind_from_arguments(**kargs)
    else:
        bind_from_arguments(args[0], **kargs)


if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '--help' or sys.argv[1] == '-h':
        logging.info("\n Run the script with a configuration file \
                        as argument, e.g.")
        logging.info("\n   ./nbbinder.py config.yml")
        logging.info("\nFor the documentation, type 'pydoc3 nbbinder.py'.\n")
    else:
        try:
            bind_from_configfile(sys.argv[1])
        except NotImplementedError:
            logging.info('provided argument is not a yaml file or not \
                          a properly formated yaml configuration file.')
