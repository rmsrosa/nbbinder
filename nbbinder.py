#!/usr/bin/env python3
"""
Gives a navigable book-like structure to a collection of Jupyter notebooks.
"""

__author__ = "Ricardo M. S. Rosa <rmsrosa@gmail.com>"
__homepage__ = "http://github.com/rmsrosa/nbbinder"
__copyright__ = """Original work Copyright (c) 2016 Jacob VanderPlas
Modified work Copyright (c) 2019 Ricardo M S Rosa
"""
__license__ = "MIT"
__version__ = "0.7a2"

import os
import re
import itertools
import sys
import logging

import yaml

import nbformat
from nbformat.v4.nbbase import new_markdown_cell

# Regular expression for indexing the notebooks
# Tested in https://regexr.com/
REG = re.compile(r'(\b\d{2}|\b[A][A-Z]|\b[B][A-Z])\.(\d{2}|\b[A][A-Z]|\b[B][A-Z]|)-(.*)\.ipynb')
REG_INSERT = re.compile(r'(\b\d{2}|\b[A][A-Z]|\b[B][A-Z])([a-z]|)\.(\d{2}|\b[A][A-Z]|\b[B][A-Z]|)([a-z]|)-(.*)\.ipynb')

# Markers for the affected notebook cells
TOC_MARKER = "<!--TABLE_OF_CONTENTS-->"    
HEADER_MARKER = "<!--HEADER-->"   
NAVIGATOR_MARKER = "<!--NAVIGATOR-->"

def indexed_notebooks(path_to_notes: str=''):
    """Returns a sorted list with the filenames of the 'indexed notebooks'.

    The notebooks are expected to be in the folder indicated by the
    argument `path_to_notes`. The "indexed notebooks" are those that
    match the regular expression REG. Filenames that do not
    match the regular expression are ignored.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.

    Returns
    -------
    : list of str
        A list with the filenames of the notebooks that match 
        the regular expression (the "indexed notebooks"),
        ordered by the lexicographycal order.
    """
    return sorted(nb for nb in os.listdir(path_to_notes) if REG.match(nb))

def is_index(g: str) -> bool:
    """Checks whether a string is an index, returning True or False.
    
    An index is a string of length two composed only of numeric or uppercase
    characters, with only 'A' and 'B' allowed in the first position of the
    string.
    """

    if type(g)==str and len(g)==2 and (g[0].isdecimal() or g[0] in ('A', 'B')) and (g[1].isdecimal() or g[1].isupper()):
        return True
    else:
        return False

def increase_index(g: str) -> str:
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
    g : str
        The index to be increased

    Returns
    -------
    : str
        The index increased by one
    
    Raises
    ------
    Exception if string is not an index

    Exception if numeric index increases beyond 99

    Exception if alphanumeric index increases beyond A9 or B9

    Exception if alphanumeric index increases beyond AZ or BZ
    """
    if not is_index(g):
        raise Exception('String is not an index')

    if g.isdecimal():
        n = int(g) + 1
        if n>99:
            raise Exception('Increasing numeric index beyond 99')
        if n>=10:
            g = str(n)
        else:
            g = '0'+str(n)
    elif g[1].isalnum():
        if g[1]==9:
            raise Exception('Increasing alphanumeric index beyond A9 or B9')
        elif g[1]=='Z':
            raise Exception('Increasing alphanumeric index beyond AZ or BZ')
        g = g[0] + chr(ord(g[1])+1)
    return g

def is_marker_cell(MARKER: str=None, 
        cell: nbformat.notebooknode.NotebookNode=None) -> bool:
    """Checks where the given cell starts with the given MARKER.
    
    Parameters
    ----------
    MARKER : str
        The MARKER to be searched for.

    cell : nbformat.notebooknode.NotebookNode
        The cell to be checked.

    Returns
    -------
    : bool
        True or False, depending on whether the MARKER exists in the
        cell or not.
    """
    return cell.source.startswith(MARKER)

def remove_marker_cells(path_to_notes: str='.', MARKER: str=None):
    """Removes any MARKER cell from the indexed notebooks in path_to_notes.
    
    Parameters
    ----------
    MARKER : str
        The MARKER to be searched for.

    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.
    """
    if MARKER:
        for nb_name in indexed_notebooks(path_to_notes):
            nb_file = os.path.join(path_to_notes, nb_name)
            nb = nbformat.read(nb_file, as_version=4)

            new_cells = []
            for cell in nb.cells:
                if not is_marker_cell(MARKER, cell):
                    new_cells.append(cell)
                else:
                    logging.info("- removing '{}' cell from {}".format(MARKER, nb_name))

            nb.cells = new_cells
            nbformat.write(nb, nb_file)

def get_notebook_title(path_to_notes: str='.', nb_name: str=None) -> str:
    """Returns the title of a juyter notebook.

    It looks for the first cell, in the notebook, that starts with
    a single markdown symbol '#' and returns the contents of the first 
    line of this cell, striped out of '# ' and the remaining lines.

    Parameters
    ----------
    nb_name : str
        The name of the jupyter notebook file.

    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.
    
    Returns
    -------
    : str
        The desired title of the notebook or None if not found.
    """
    nb = nbformat.read(os.path.join(path_to_notes, nb_name), as_version=4)
    for cell in nb.cells:
        if cell.source.startswith('#'):
            return cell.source[1:].splitlines()[0].strip()


def get_notebook_full_entry(path_to_notes: str='.', nb_name: str=None) -> list:
    """Returns the full entry of a notebook.
    
    This entry is to be used for the link to the notebook from the
    table of contents and from the navigators.

    Parameters
    ----------
    nb_name : str
        The name of the jupyter notebook file.

    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.

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
    chapter, section, basename = REG.match(nb_name).groups()

    if chapter.isdecimal():
        chapter_clean = int(chapter)
    else:
        chapter_clean = chapter[1]
    title = get_notebook_title(path_to_notes, nb_name)

    if chapter=='00' or chapter[0]=='B' or section=='':
        markdown_entry = '### '
        num_entry = ''
    elif section=='00':
        markdown_entry = '### '
        num_entry = '{}. '.format(chapter_clean)
    else:
        markdown_entry = '&nbsp;&nbsp;&nbsp;&nbsp; '
        num_entry = '{}.{}. '.format(chapter_clean, int(section))
    
    return markdown_entry, num_entry, title

def get_notebook_entry(path_to_notes: str='.', nb_name: str=None, 
        show_index: bool = True) -> list:
    """Returns the entry of a notebook.
    
    This entry is to be used for the link to the notebook from the
    table of contents and from the navigators. Depending on the
    value of the argument `show_index`, the entry can be either 
    the full entry provided by the function `get_notebook_full_entry()`
    or simply the title of the notebook, provided by the function
    `get_notebook_title()`.

    Parameters
    ----------
    nb_name : str
        The name of the jupyter notebook file. 

    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.

    show_index : boolean
        Indicates whether to include the chapter and section numbers
        of the notebook in the table of contents (if True) or just 
        the title (if False).

    Returns
    -------
    markdown_entry : str
        The type of markdown header or identation for the entry in
        Table of Contents
    
    entry : str
        A string with the entry name.
    """
    if show_index:
        entry = ''.join(list(get_notebook_full_entry(path_to_notes, nb_name)[1:3]))
    else:
        entry = get_notebook_title(path_to_notes, nb_name)
    return entry   

def yield_contents(path_to_notes: str='.', show_index_in_toc: bool=True):
    """Generator function with entries for each of the indexed notebooks.

    It takes all the indexed notebooks and it creates a generator 
    function to iterate from one notebook to the next, returning, 
    each time, the navigator entry associated with that notebook.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.

    show_index_in_toc : bool
        Whether to display the navigator with the chapter
        and section number of each notebook or just their title.

    Yields
    ------
    : str
        Next navigator entry in the iterator
    """
    for nb_name in indexed_notebooks(path_to_notes):
        markdown_entry, num_entry, title = get_notebook_full_entry(path_to_notes, nb_name)
        if show_index_in_toc:
            yield '{}[{}]({})\n'.format(markdown_entry, num_entry + title, nb_name)
        else:
            yield '{}[{}]({})\n'.format(markdown_entry, title, nb_name)

def get_contents(path_to_notes: str='.', show_index_in_toc: bool=True):
    """Returns the 'Table of Contents'.

    Returns a string with the 'Table of Contents' constructed 
    from the collection of notebooks in the folder indicated by
    the argument `path_to_notes`.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.

    show_index_in_toc : bool
        Whether to display the table of contents with the chapter
        and section number of each notebook or just their title.

    Returns
    -------
    : str
    The table of contents.
    """

    contents = ""
    for item in yield_contents(path_to_notes, show_index_in_toc):
        contents += item + "\n"
    
    return contents


def insert_notebooks(path_to_notes: str='.'):
    """Includes a notebook in the colllection.

    Checks whether there is any notebook that matches the regular expression
    indicating it is to be incuded in the collection of indexed notebooks 
    and, if so, renames the affected notebooks in the appropriate order.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.
    """

    nb_names_ins = sorted(nb for nb in os.listdir(path_to_notes) if REG_INSERT.match(nb))
    nb_names_new = nb_names_ins.copy()
    additions = [1 if REG_INSERT.match(nb).group(2) 
                    or REG_INSERT.match(nb).group(4) 
                    else 0 for nb in nb_names_ins]

    for j in range(len(nb_names_ins)):
        nbj_reg = REG_INSERT.match(nb_names_new[j])
        if nbj_reg.group(4):
            for k in range(j,len(nb_names_ins)):
                nbk_reg = REG_INSERT.match(nb_names_new[k])
                if nbk_reg.group(1,2) == nbj_reg.group(1,2):
                    gk3 = nbk_reg.group(3)
                    if nbk_reg.group(1,2,3,4) == nbj_reg.group(1,2,3,4):
                        gk3_new = increase_index(gk3)
                        gk4_new = ''
                    else:
                        gk3_new = increase_index(gk3)
                        gk4_new = nbk_reg.group(4)
                    nb_names_new[k] = nbk_reg.group(1) + nbk_reg.group(2) + '.' + gk3_new + gk4_new + '-' + nbk_reg.group(5) + '.ipynb'
        if nbj_reg.group(2):
            nb_names_new[j] = nb_names_new[j][:nbj_reg.start(2)] + nb_names_new[j][nbj_reg.end(2):]
            for k in range(j,len(nb_names_ins)):
                nbk_reg = REG_INSERT.match(nb_names_new[k])
                if nbk_reg.group(1)[0] == nbj_reg.group(1)[0]: 
                    gk1_new = increase_index(nbk_reg.group(1))
                    if nbk_reg.group(1,2) == nbj_reg.group(1,2):
                        gk2_new = ''
                    else:
                        gk2_new = nbk_reg.group(2)
                    nb_names_new[k] = gk1_new + gk2_new + '.' + nbk_reg.group(3) + nbk_reg.group(4) + '-' + nbk_reg.group(5) + '.ipynb'

    if nb_names_new == nb_names_ins:
        logging.info('- no files need renaming, no reindexing needed')
        logging.info('- no files need renaming, no reindexing needed')
    else:
        count = 0
        for f, f_new in zip(nb_names_ins, nb_names_new):
            count +=1
            if f != f_new:
                logging.info('- replacing {0} with {1}'.format(f, f_new))
                logging.info('- replacing {0} with {1}'.format(f, f_new))
            os.rename(os.path.join(path_to_notes, f), os.path.join(path_to_notes, str(count) + '-' + f_new))
        count = 0
        for f_new in nb_names_new:
            count +=1
            os.rename(os.path.join(path_to_notes, str(count) + '-' + f_new), os.path.join(path_to_notes, f_new))

def tighten_notebooks(path_to_notes: str='.'):
    """Tighten the indexes of the notebooks in the colllection.

    Checks whether there are gaps in the indices of the notebooks
    and, if so, renames the affected notebooks in the appropriate 
    order.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.
    """

    nb_names = sorted(nb for nb in os.listdir(path_to_notes) if REG.match(nb))
    nb_names_new = nb_names.copy()

    nb_reg = [REG.match(nb_names[j]) for j in range(len(nb_names))]
    nb_new_reg = nb_reg.copy()

    for j in range(len(nb_names)):
        if j==0:
            if (nb_reg[j].group(1).isdecimal() 
                    and nb_reg[j].group(1)>='02'):
                nb_names_new[j] = '01.' + nb_reg[j].group(2) \
                    + '-' + nb_reg[j].group(3) + '.ipynb'
            elif (nb_reg[j].group(1).isalpha()
                    and nb_reg[j].group(1)[1]>='B'):
                nb_names_new[j] = nb_reg[j].group(1)[0] \
                    + 'A.' + nb_reg[j].group(2) \
                    + '-' + nb_reg[j].group(3) + '.ipynb'
            elif (nb_reg[j].group(1).isalnum()
                    and nb_reg[j].group(1)[1]>='2'):
                nb_names_new[j] = nb_reg[j].group(1)[0] \
                    + '1.' + nb_reg[j].group(2) \
                    + '-' + nb_reg[j].group(3) + '.ipynb'
        else:
            if (nb_reg[j].group(1).isdecimal() 
                    and nb_reg[j].group(1)>='02'):               
                if nb_reg[j].group(1) == nb_reg[j-1].group(1):
                    nb_names_new[j] = nb_new_reg[j-1].group(1) \
                        + '.' + nb_reg[j].group(2) \
                        + '-' + nb_reg[j].group(3) + '.ipynb'
                elif (nb_reg[j].group(1)
                        >increase_index(nb_new_reg[j-1].group(1))):
                    nb_names_new[j] = \
                        increase_index(nb_new_reg[j-1].group(1)) \
                        + '.' + nb_reg[j].group(2) \
                        + '-' + nb_reg[j].group(3) + '.ipynb'
            elif (nb_reg[j].group(1)[0] in ('A', 'B')
                    and nb_reg[j].group(1)[1]>='B'):
                if (nb_reg[j].group(1)[0]=='A' 
                        and nb_new_reg[j-1].group(1).isdecimal()):
                    nb_names_new[j] = 'AA.' + nb_reg[j].group(2) \
                        + '-' + nb_reg[j].group(3) + '.ipynb'
                elif (nb_reg[j].group(1)[0]=='B' 
                        and nb_new_reg[j-1].group(1)[0]=='A'):
                    nb_names_new[j] = 'BA.' + nb_reg[j].group(2) \
                        + '-' + nb_reg[j].group(3) + '.ipynb'    
                elif nb_reg[j].group(1) == nb_reg[j-1].group(1):
                    nb_names_new[j] = nb_new_reg[j-1].group(1) \
                        + '.' + nb_reg[j].group(2) \
                        + '-' + nb_reg[j].group(3) + '.ipynb'
                elif (nb_reg[j].group(1)
                        >increase_index(nb_new_reg[j-1].group(1))):
                    nb_names_new[j] = \
                        increase_index(nb_new_reg[j-1].group(1)) \
                        + '.' + nb_reg[j].group(2) \
                        + '-' + nb_reg[j].group(3) + '.ipynb'
        nb_new_reg[j] = REG.match(nb_names_new[j])

    nb_names_newest = nb_names_new.copy()

    nb_new_reg = [REG.match(nb_names_new[j]) for j in range(len(nb_names_new))]
    nb_newest_reg = nb_new_reg.copy()

    for j in range(len(nb_names_new)):
        if j==0 or nb_new_reg[j].group(1)!=nb_new_reg[j-1].group(1):
            if (nb_new_reg[j].group(2).isdecimal() 
                    and nb_new_reg[j].group(2)>='02'):
                nb_names_newest[j] = nb_new_reg[j].group(1) \
                    + '.01-' + nb_new_reg[j].group(3) + '.ipynb'
            elif (nb_new_reg[j].group(2)[0]=='A'
                    and nb_new_reg[j].group(2)[1]>='B'):
                nb_names_newest[j] = nb_new_reg[j].group(1) \
                    + '.AA-' + nb_new_reg[j].group(3) + '.ipynb'
            elif (nb_new_reg[j].group(2)=='B'
                    and nb_new_reg[j].group(2)[1]>='B'):
                nb_names_newest[j] = nb_new_reg[j].group(1) \
                    + '.BA-' + nb_new_reg[j].group(3) + '.ipynb'
        else:
            if (nb_new_reg[j].group(2).isdecimal() 
                    and nb_new_reg[j].group(2)
                        >increase_index(nb_newest_reg[j-1].group(2))):
                    nb_names_newest[j] = nb_new_reg[j].group(1) + '.' \
                        + increase_index(nb_newest_reg[j-1].group(2)) \
                        + '-' + nb_new_reg[j].group(3) + '.ipynb'
            elif (nb_new_reg[j].group(2)[0] in ('A', 'B')
                    and nb_new_reg[j].group(2)[1]>='B'):
                if (nb_new_reg[j].group(2)[0]=='A' 
                        and nb_newest_reg[j-1].group(2).isdecimal()):
                    nb_names_newest[j] = nb_new_reg[j].group(1) \
                        + '.AA-' + nb_new_reg[j].group(3) + '.ipynb'
                elif (nb_new_reg[j].group(2)[0]=='B' 
                        and nb_newest_reg[j-1].group(1)[0]!='B'):
                    nb_names_newest[j] = nb_new_reg[j].group(1) \
                        + '.BA-' + nb_new_reg[j].group(3) + '.ipynb'    
                elif (nb_new_reg[j].group(2)
                        >increase_index(nb_newest_reg[j-1].group(2))):
                    nb_names_newest[j] = nb_new_reg[j].group(1) + '.' \
                        + increase_index(nb_newest_reg[j-1].group(2)) \
                        + '-' + nb_new_reg[j].group(3) + '.ipynb'
        nb_newest_reg[j] = REG.match(nb_names_newest[j])

    if nb_names_newest == nb_names:
        logging.info('- no files need renaming, no reindexing needed')
        logging.info('- no files need renaming, no reindexing needed')
    else:
        count = 0
        for f, f_newest in zip(nb_names, nb_names_newest):
            count +=1
            if f != f_newest:
                logging.info('- replacing {0} with {1}'.format(f, f_newest))
                logging.info('- replacing {0} with {1}'.format(f, f_newest))
            os.rename(os.path.join(path_to_notes, f), os.path.join(path_to_notes, str(count) + '-' + f_newest))
        count = 0
        for f_newest in nb_names_newest:
            count +=1
            os.rename(os.path.join(path_to_notes, str(count) + '-' + f_newest), os.path.join(path_to_notes, f_newest))

def reindex(path_to_notes: str='.', insert: bool=True, tighten: bool=False):

    if insert:
        insert_notebooks(path_to_notes)
    
    if tighten:
        tighten_notebooks(path_to_notes)


def add_contents(path_to_notes: str='.', toc_nb_name: str=None,
        toc_title: str='', show_index_in_toc: bool=True):
    """Adds the table of contentes to a selected notebook.

    It adds the table of contents, generated from the collection of 
    notebooks in the directory `path_to_notes`, to the notebook 
    `toc_nb_name`. The inclusion, or not, of the Chapter and Section 
    numbers in the table of contents is indicaded by the argument `show_index_in_toc`.

    Parameters
    ----------
    toc_nb_name : str
        filename of the notebook in which the table of contents
        is to be inserted

    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.

    show_index_in_toc : bool
        Whether to display the navigator with the chapter
        and section number of each notebook or just their title.
    """
    # error handling
    assert(type(path_to_notes)==str), "Argument `path_to_notes` should be a string"
    assert(type(toc_nb_name)==str), "Argument `toc_nb_name` should be a string"
    assert(type(toc_title)==str), "Argument `toc_title` should be a string"

    contents = TOC_MARKER + "\n## [" + toc_title + "](#)\n\n"
    for item in yield_contents(path_to_notes, show_index_in_toc):
        contents += item + "\n"

    toc_nb_file = os.path.join(path_to_notes, toc_nb_name)

    toc_nb = nbformat.read(toc_nb_file, as_version=4)

    toc_cell_found = False
    for cell in toc_nb.cells:
        if is_marker_cell(TOC_MARKER, cell):
            cell.source = contents
            toc_cell_found = True
            
    if toc_cell_found:
        nbformat.write(toc_nb, toc_nb_file)
        logging.info('- Table of contents updated in {}'.format(toc_nb_name))
    else:
        logging.info('* No markdown cell starting with {} found in {}'.format(TOC_MARKER, toc_nb_name))
        logging.info("- inserting table of contents in {0}".format(toc_nb_name))
        if toc_nb.cells and is_marker_cell(NAVIGATOR_MARKER, toc_nb.cells[-1]):
            toc_nb.cells.insert(-1, new_markdown_cell(source=contents))
        else:
            toc_nb.cells.append(new_markdown_cell(source=contents))

    nbformat.write(toc_nb, toc_nb_file)

def add_headers(path_to_notes: str='.', header: str=None):
    """Adds header to each notebook in the collection.

    It adds the provided `header`as the first cell of each notebook
    in the collection of indexed notebooks in the folder `path_to_notes`.

    Parameters
    ----------
    header : str
        The string with the contents to be included in the header cell.

    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.
    """
    for nb_name in indexed_notebooks(path_to_notes):
        nb_file = os.path.join(path_to_notes, nb_name)
        nb = nbformat.read(nb_file, as_version=4)

        if nb.cells and is_marker_cell(HEADER_MARKER, nb.cells[0]):    
            logging.info('- updating header for {0}'.format(nb_name))
            nb.cells[0].source = HEADER_MARKER + '\n' + header
        else:
            logging.info('- inserting header for {0}'.format(nb_name))
            nb.cells.insert(0, new_markdown_cell(HEADER_MARKER + '\n' + header))
        nbformat.write(nb, nb_file)

def prev_this_next(collection):
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
    a, b, c = itertools.tee(collection,3)
    next(c)
    return zip(itertools.chain([None], a), b, itertools.chain(c, [None]))

def get_navigator_entries(path_to_notes: str='.', 
        core_navigators: list=[], 
        user: str='', repository: str='', 
        branch: str='master', 
        github_nb_dir: str='.', 
        extra_badges: list=None,
        show_index_in_nav: bool=True):
    """Iterable with the navigator info for each notebook.

    It reads the indexed notebooks in the folder `path_to_notes` and 
    generates an iterable with the information needed to build the
    navigators for each notebook.

    Parameters
    ----------
    core_navigators : list of str
        A lists of strings with the filenames of each notebook to be
        included in the navigators, in between the links to the
        "previous" and the "next" notebooks. It defaults to the empty
        list.

    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.

    user : str
        The github username of the onwer of the repository in which 
        the notebooks reside, in case one wants to add a badge to 
        open up the notebooks in one of the configured cloud 
        computing platforms (google colab and binder). It defaults to 
        the empty string.

    repository : str
        The name of the github repository mentioned in the description 
        of the `user` argument. It defaults to the empty string.

    branch : str
        The name of the branch of the github repository mentioned in
        the description of the `user` argument. It defaults to 'master'.

    github_nb_dir : str
        The path to the notebooks, from the root directory of the
        repository mentioned in the description of the `user` argument.  
        It defaults to '.'.

    extra_badges : list of dict

    show_index_in_nav : bool
        Whether to display the navigator with the chapter
        and section number of each notebook or just their title.
        It defaults to True.

    Yields
    ------
    : str
        Path to current notebook in the iterator.
    : str
        Contents of the navigation bar for the current notebook in the
        iterator.
    : str
        The google colab link for the current notebook in the iterator.
    : str
        The binder link for the current notebook in the iterator.
    : str
        The extra badge link for the current notebook in the iterator.      
    """
    PREV_TEMPLATE = "[<- {title}]({url}) "
    CENTER_TEMPLATE = "| [{title}]({url}) "
    NEXT_TEMPLATE = "| [{title} ->]({url})"

    COLAB_LINK = """
<a href="https://colab.research.google.com/github/{user}/{repository}/blob/{branch}/{github_nb_dir}/{notebook_filename}"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Google Colab" title="Open in Google Colab"></a>
"""
    BINDER_LINK = """
<a href="https://mybinder.org/v2/gh/{user}/{repository}/{branch}?filepath={github_nb_dir}/{notebook_filename}"><img align="left" src="https://mybinder.org/badge.svg" alt="Open in binder" title="Open in binder"></a>
"""
    EXTRA_BADGE_LINK = """
 <a href="{badge_url}/{badge_filename}"><img align="left" src="https://img.shields.io/badge/{badge_label}-{badge_message}-{badge_color}" alt="{badge_alt_title}" title="{badge_alt_title}"></a>
"""   

    for prev_nb, this_nb, next_nb in prev_this_next(indexed_notebooks(path_to_notes)):
        navbar = ""
        if prev_nb:
            entry = get_notebook_entry(path_to_notes, prev_nb, 
                                       show_index_in_nav)
            navbar += PREV_TEMPLATE.format(title=entry, url=prev_nb)

        for center_nb in core_navigators:
            entry = get_notebook_entry(path_to_notes, center_nb, 
                                       show_index_in_nav)
            navbar += CENTER_TEMPLATE.format(title=entry, url=center_nb)

        if next_nb:
            entry = get_notebook_entry(path_to_notes, next_nb, 
                                       show_index_in_nav)
            navbar += NEXT_TEMPLATE.format(title=entry, url=next_nb)

        this_colab_link = COLAB_LINK.format(user=user,
            repository=repository, 
            branch=branch, github_nb_dir=github_nb_dir, 
            notebook_filename=os.path.basename(this_nb))

        this_binder_link = BINDER_LINK.format(user=user,
            repository=repository, 
            branch=branch, github_nb_dir=github_nb_dir, 
            notebook_filename=os.path.basename(this_nb))

        if extra_badges:
            this_extra_badge_link = EXTRA_BADGE_LINK.format(
                badge_url=extra_badges[0]['url'],
                badge_filename=this_nb.replace('.ipynb',
                    extra_badges[0]['extension']),
                badge_label=extra_badges[0]['label'],
                badge_message=extra_badges[0]['message'],
                badge_color=extra_badges[0]['color'],
                badge_alt_title=extra_badges[0]['alt_title'])
        else:
            this_extra_badge_link=''
            
        yield os.path.join(path_to_notes, this_nb), navbar, this_colab_link, this_binder_link, this_extra_badge_link

def add_navigators(path_to_notes: str='.', core_navigators: list=[], 
        user: str='', repository: str='', branch: str='master', 
        github_nb_dir: str='.', 
        extra_badges: list=None,
        show_colab: bool=False, show_binder: bool=False, 
        show_extra_badge: bool=False,
        show_index_in_nav: bool=True):
    """Adds navigators to each notebook in the collection.

    Adds top and bottom navigators to each notebook in the collection 
    of indexed notebooks in the folder `path_to_notes`.

    Parameters
    ----------
    core_navigators : list of str
        A lists of strings with the filenames of each notebook to be
        included in the navigators, in between the links to the
        "previous" and the "next" notebooks. It defaults to the empty
        list.

    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.

    user : str
        The github username of the onwer of the repository in which 
        the notebooks reside, in case one wants to add a badge to 
        open up the notebooks in one of the configured cloud 
        computing platforms (google colab and binder). It defaults to 
        the empty string.

    repository : str
        The name of the github repository mentioned in the description 
        of the `user` argument. It defaults to the empty string.

    branch : str
        The name of the branch of the github repository mentioned in
        the description of the `user` argument. It defaults to 'master'.

    github_nb_dir : str
        The path to the notebooks, from the root directory of the
        repository mentioned in the description of the `user` argument.  
        It defaults to '.'.

    extra_badge_url : str
    extra_badge_replace_nb_extension : str
    extra_badge_label : str
    extra_badge_message : str
    extra_badge_color : str
    extra_badge_alt_title : str

    show_colab : bool
        Whether to display the Google Colab badge or not. It defaults
        to False.

    show_binder : bool
        Whether to display the Binder badge or not. It defaults
        to False.

    show_extra_badge : bool
        Whether to display an Extra badge or not. It defaults
        to False.

    show_index_in_nav : bool
        Whether to display the navigator with the chapter
        and section number of each notebook or just their title.
        It defaults to True.
    """
    for nb_file, navbar, this_colab_link, this_binder_link, this_extra_badge_link in get_navigator_entries(path_to_notes,
            core_navigators, 
            user, repository, branch, 
            github_nb_dir, 
            extra_badges,
            show_index_in_nav):
        nb = nbformat.read(nb_file, as_version=4)
        nb_name = os.path.basename(nb_file)

        navbar_top = navbar_bottom = NAVIGATOR_MARKER + "\n"
        navbar_bottom = NAVIGATOR_MARKER + "\n\n---\n" + navbar

        if show_colab or show_binder or show_extra_badge:
            navbar_bottom += "\n"

        if show_colab:
            navbar_top += this_colab_link + "&nbsp;"
            navbar_bottom += this_colab_link

        if show_binder:
            navbar_top += this_binder_link + "&nbsp;"
            navbar_bottom += this_binder_link

        if show_extra_badge:
            navbar_top += this_extra_badge_link + "&nbsp;"
            navbar_bottom += this_extra_badge_link

        if show_colab or show_binder or show_extra_badge:
            navbar_top += "\n"
            navbar_bottom += "&nbsp;"

        navbar_top += "\n" + navbar + "\n\n---\n"

        if len(nb.cells) > 1 and is_marker_cell(NAVIGATOR_MARKER, nb.cells[1]):         
            logging.info("- updating navbar for {0}".format(nb_name))
            nb.cells[1].source = navbar_top
        else:
            logging.info("- inserting navbar for {0}".format(nb_name))
            nb.cells.insert(1, new_markdown_cell(source=navbar_top))

        if len(nb.cells)>2 and is_marker_cell(NAVIGATOR_MARKER, nb.cells[-1]):
            nb.cells[-1].source = navbar_bottom
        else:
            nb.cells.append(new_markdown_cell(source=navbar_bottom))
        nbformat.write(nb, nb_file)

def bind_from_arguments(path_to_notes: str='.', 
        insert: bool=False,
        tighten: bool=False,
        toc_nb_name: str='', 
        toc_title: str='',
        header: str='', 
        core_navigators: str='',
        user: str='', repository: str='', branch: str='master', 
        github_nb_dir: str='.', 
        extra_badges: list=None,
        show_colab: bool=False, show_binder: bool=False, 
        show_extra_badge: bool=False,
        show_index_in_toc: bool=True,
        show_index_in_nav: bool=True):
    """Binds the collection of notebooks from the arguments provided.

    Parameters
    ----------
    path_to_notes : str
        The path to the directory that contains the notebooks, 
        either the absolute path or the path relative from 
        where the code is being ran. It defaults to '.'.

    insert : bool
        Indicates whether to insert notebooks in the collection of
        indexed notebooks or not. It defaults to False.

    tighten : bool
        Indicates whether to tighten the indices of the notebooks,
        i.e. whether there are gaps in the indices of the notebooks
        and, if so, rename the affected notebooks in the 
        appropriate order. It defaults to False.

    toc_nb_name : str
        Filename of the notebook in which the table of contents
        is to be inserted

    toc_title : str
        Text to be displayed as a title for the table of contents cell, 
        e.g. 'Contents', 'Table of Contents', or in other languages, 
        'Conteúdo', 'Table des Matières', and so on.

    header : str
        The string with the contents to be included in the header cell.

    core_navigators : list of str
        A lists of strings with the filenames of each notebook to be
        included in the navigators, in between the links to the
        "previous" and the "next" notebooks. It defaults to the empty
        list.

    user : str
        The github username of the onwer of the repository in which 
        the notebooks reside, in case one wants to add a badge to 
        open up the notebooks in one of the configured cloud 
        computing platforms (google colab and binder). It defaults to 
        the empty string.

    repository : str
        The name of the github repository mentioned in the description 
        of the `user` argument. It defaults to the empty string.

    branch : str
        The name of the branch of the github repository mentioned in
        the description of the `user` argument. It defaults to 'master'.

    github_nb_dir : str
        The path to the notebooks, from the root directory of the
        repository mentioned in the description of the `user` argument.  
        It defaults to '.'.

    extra_badge_url : str
    extra_badge_replace_nb_extension : str
    extra_badge_label : str
    extra_badge_message : str
    extra_badge_color : str
    extra_badge_alt_title : str

    show_colab : bool
        Whether to display the Google Colab badge or not. It defaults
        to False.

    show_binder : bool
        Whether to display the Binder badge or not. It defaults
        to False.

    show_extra_badge : bool
        Whether to display an Extra badge or not. It defaults
        to False.

    show_index_in_toc : bool
        Whether to display the navigator with the chapter
        and section number of each notebook or just their title.

    show_index_in_nav : bool
        Whether to display the navigator with the chapter
        and section number of each notebook or just their title.
        It defaults to True.
    """

    if insert or tighten:
        reindex(path_to_notes, insert, tighten)

    remove_marker_cells(path_to_notes, HEADER_MARKER)
    remove_marker_cells(path_to_notes, NAVIGATOR_MARKER)

    add_contents(path_to_notes=path_to_notes, 
        toc_nb_name=toc_nb_name,
        toc_title=toc_title, 
        show_index_in_toc=show_index_in_toc)

    add_headers(path_to_notes=path_to_notes, header=header)

    add_navigators(path_to_notes=path_to_notes, 
        core_navigators=core_navigators,
        user=user, 
        repository=repository, branch=branch, 
        github_nb_dir=github_nb_dir,
        extra_badges = extra_badges,
        show_colab=show_colab, 
        show_binder=show_binder,
        show_extra_badge=show_extra_badge,
        show_index_in_nav=show_index_in_nav)

def bind_from_configfile(config_file: str):
    """Binds the collection of notebooks from a configuration file.

    It reads the given configuration file in YAML format and pass 
    the arguments in the configuration file to the function
    `bind_from_arguments()`.

    Parameters
    ----------
    config_file : str
        The filename of the configuration file.
    """
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    if 'path_to_notes' in config:
        path_to_notes = config['path_to_notes']
    else:
        path_to_notes = '.'

    if 'reindexing' in config:
        reindex(path_to_notes, **config['reindexing'])

    remove_marker_cells(path_to_notes, HEADER_MARKER)
    remove_marker_cells(path_to_notes, NAVIGATOR_MARKER)

    if 'contents' in config:
        add_contents(path_to_notes=path_to_notes, **config['contents'])

    if 'header' in config:
        add_headers(path_to_notes=path_to_notes, header=config['header'])

    if 'navigators' and 'badges' in config:
        add_navigators(path_to_notes=path_to_notes, **config['navigators'],
            **config['badges'])
    elif 'navigators' in config:
        add_navigators(path_to_notes=path_to_notes, **config['navigators'])
    elif 'badges' in config:
        add_navigators(path_to_notes=path_to_notes, **config['badges'])        

def bind(*args, **kargs):
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
    if len(args) > 0 and args[0].endswith(('.yml', '.yaml')):
        bind_from_configfile(args[0])
    elif 'path_to_notes' in kargs.keys():
        bind_from_arguments(**kargs)
    else:
        bind_from_arguments(args[0], **kargs)

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '--help' or sys.argv[1] == '-h':
        logging.info("\n Run the script with a configuration file as argument, e.g.")
        logging.info("\n   ./nbbinder.py config.yml")
        logging.info("\nFor the documentation, type 'pydoc3 nbbinder.py'.\n")
    else:
        try:
            bind_from_configfile(sys.argv[1])
        except NotImplementedError:
            logging.info('provided argument is not a yaml file or not a properly formated yaml configuration file.')
