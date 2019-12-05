#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Generates a navigable book-like structure to a collection of Jupyter notebooks.
'''

__author__ = "Ricardo M. S. Rosa <rmsrosa@gmail.com>"
__homepage__ = "http://github.com/rmsrosa/nbbinder"
__copyright__ = '''
Original work Copyright (c) 2016 Jacob VanderPlas
Modified work Copyright (c) 2019 Ricardo M S Rosa
'''
__license__ = "MIT"
__version__ = "0.5.1"
__status__ = "beta"

import os
import re
import itertools
import sys

import yaml

import nbformat
from nbformat.v4.nbbase import new_markdown_cell

# Regular expression for indexing the notebooks
# Tested in https://regexr.com/
REG = re.compile(r'(\b\d\d|\b[A][A-Z]|\b[B][A-Z])\.(\d{2}|)-(.*)\.ipynb')
REG_STAR = re.compile(r'(\b\d\d|\b[A][A-Z]|\b[B][A-Z])([a-z]+|)\.(\d{2}|)([a-z]+|)-(.*)\.ipynb')

TOC_MARKER = "<!--TABLE_OF_CONTENTS-->"    
HEADER_MARKER = "<!--HEADER-->"   
NAVIGATOR_MARKER = "<!--NAVIGATOR-->"

def indexed_notebooks(app_to_notes_path='.'):
    '''
    Returns a sorted list with the filenames of the 'indexed notebooks'
    in the given 'app_to_notes_path'. The 'indexed notebooks' are those that
    match the regular expression REG. Filenames that do not
    match the regular expression are ignored.

    Argument:
    ---------
        app_to_notes_path: string
            The path to the directory that contains the notebooks, 
            either the absolute path or the path relative from 
            where the code is being ran.

    Returns:
    -------
        : list of strings
            A list with the filenames of the notebooks that match 
            the regular expression (the 'indexed notebooks'), 
            ordered by the lexicographycal order.

    Raises:
    -------
    
    '''
    return sorted(nb for nb in os.listdir(app_to_notes_path) if REG.match(nb))

def increase_group(g:str):
    if g.isdecimal():
        n = int(g) + 1
        if n>=10:
            g = str(n)
        else:
            g = '0'+str(n)
    elif g[1].isalnum():
        g = g[0] + chr(ord(g[1])+1)
    return g

def restructure(app_to_notes_path='.'):
    '''
    Check whether there is any notebook with one or more star characters ('*')
    in the third regular expression group, indicating it is to be included in
    the collection, and, if so, rename the affected notebooks in the
    appropriate order.

    Argument:
    ---------
        app_to_notes_path: string
            The path to the directory that contains the notebooks, 
            either the absolute path or the path relative from 
            where the code is being ran.

    '''

    nbfiles = sorted(nb for nb in os.listdir(app_to_notes_path) if REG_STAR.match(nb))
    nbfiles_new = nbfiles.copy()
    additions = [1 if REG_STAR.match(nb).group(2) or REG_STAR.match(nb).group(4) else 0 for nb in nbfiles]
#    print('additions:', sum(additions))

    if sum(additions):
#        print('len:', len(nbfiles))
        for j in range(len(nbfiles)):
            nbj_reg = REG_STAR.match(nbfiles_new[j])
            if nbj_reg.group(4):
#                print('j in group 4:', j)
                for k in range(j,len(nbfiles)):
                    nbk_reg = REG_STAR.match(nbfiles_new[k])
                    if nbk_reg.group(1,2) == nbj_reg.group(1,2):
#                        print('k:', k)
                        gk3 = nbk_reg.group(3)
                        if nbk_reg.group(1,2,3,4) == nbj_reg.group(1,2,3,4):
                            gk3_new = increase_group(gk3)
                            gk4_new = ''
                        else:
                            gk3_new = increase_group(gk3)
                            gk4_new = nbk_reg.group(4)
                        nbfiles_new[k] = nbk_reg.group(1) + nbk_reg.group(2) + '.' + gk3_new + gk4_new + '-' + nbk_reg.group(5) + '.ipynb'
#                    print('nbfiles_new[k]:', nbfiles_new[k])
            if nbj_reg.group(2):
#                print('j in group 2:', j)
                nbfiles_new[j] = nbfiles_new[j][:nbj_reg.start(2)] + nbfiles_new[j][nbj_reg.end(2):]
                for k in range(j,len(nbfiles)):
#                    print('k:', k)
                    nbk_reg = REG_STAR.match(nbfiles_new[k])
                    if nbk_reg.group(1)[0] == nbj_reg.group(1)[0]: 
                        gk1_new = increase_group(nbk_reg.group(1))
                        if nbk_reg.group(1,2) == nbj_reg.group(1,2):
                            gk2_new = ''
                        else:
                            gk2_new = nbk_reg.group(2)
                        nbfiles_new[k] = gk1_new + gk2_new + '.' + nbk_reg.group(3) + nbk_reg.group(4) + '-' + nbk_reg.group(5) + '.ipynb'
#                    print('nbfiles_new[k]:', nbfiles_new[k])

    if nbfiles == nbfiles_new:
        print('- no files need renaming, no restructuring needed')
    else:
        count = 0
        for f, f_new in zip(nbfiles, nbfiles_new):
            count +=1
            if f != f_new:
                print(f'- replacing {f} with {f_new}')
            os.rename(os.path.join(app_to_notes_path, f), os.path.join(app_to_notes_path, str(count) + '-' + f_new))
        count = 0
        for f_new in nbfiles_new:
            count +=1
            os.rename(os.path.join(app_to_notes_path, str(count) + '-' + f_new), os.path.join(app_to_notes_path, f_new))

    return


def is_marker_cell(MARKER, cell):
    return  cell.source.startswith(MARKER)

def remove_marker_cell(MARKER, app_to_notes_path='.'):
    for nb_name in indexed_notebooks(app_to_notes_path):
        nb_file = os.path.join(app_to_notes_path, nb_name)
        nb = nbformat.read(nb_file, as_version=4)

        new_cells = []
        for cell in nb.cells:
            if not is_marker_cell(MARKER, cell):
                new_cells.append(cell)
            else:
                print(f"- removing '{MARKER}' cell from {nb_name}")

        nb.cells = new_cells
        nbformat.write(nb, nb_file)

def get_notebook_title(nb_name, app_to_notes_path='.'):
    '''
    Returns the title of a juyter notebook.

    It looks for the first cell, in the notebook, that starts with
    the markdown symbol '#' and returns the contents of the first line
    of this cell, striped out of '#' and the remaining lines.

    Input:
    ------
        nb_name: string
            The name of the jupyter notebook file.
        app_to_notes_path: string
            The path to the directory that contains the notebooks, 
            either the absolute path or the path relative from 
            where the code is being ran.
    
    Output:
    -------
        : string
            The desired title of the notebook or None if not found.

    '''
    nb = nbformat.read(os.path.join(app_to_notes_path, nb_name), as_version=4)
    for cell in nb.cells:
        if cell.source.startswith('#'):
            return cell.source[1:].splitlines()[0].strip()


def get_notebook_full_entry(nb_name, app_to_notes_path='.'):
    '''
    Returns the entry of a notebook to be used in the Table of Contents

    Input:
    ------
        nb_name: string
            The name of the jupyter notebook file. 
        app_to_notes_path: string
            The path to the directory that contains the notebooks, 
            either the absolute path or the path relative from 
            where the code is being ran.

    Output:
    -------
        markdown_entry: string
            The type of markdown header or identation for the entry in
            Table of Contents
        
        notebook_entry: strings
            The full notebook entry, with the title, preceeded, 
            depending on the case, of the Chapter and Section numbers
            or letters.

    '''
    chapter, section, basename = REG.match(nb_name).groups()

    if chapter.isdecimal():
        chapter_clean = int(chapter)
    else:
        chapter_clean = chapter[1]
    title = get_notebook_title(nb_name, app_to_notes_path)

    if chapter=='00' or chapter[0]=='B' or section=='':
        markdown_entry = '### '
        num_entry = ''
    elif section=='00':
        markdown_entry = '### '
        num_entry = f'{chapter_clean}. '
    else:
        markdown_entry = '&nbsp;&nbsp;&nbsp;&nbsp; '
        num_entry = f'{chapter_clean}.{int(section)}. '
    
    return markdown_entry, num_entry, title

def get_notebook_entry(nb_name, app_to_notes_path='.', 
                       show_full_entry=True):
    if show_full_entry:
        entry = ''.join(list(get_notebook_full_entry(nb_name, app_to_notes_path)[1:3]))
    else:
        entry = get_notebook_title(nb_name, app_to_notes_path)
    return entry   

def yield_contents(app_to_notes_path='.', show_full_entry_in_toc=True):
    for nb_name in indexed_notebooks(app_to_notes_path):
        markdown_entry, num_entry, title = get_notebook_full_entry(nb_name, app_to_notes_path)
        if show_full_entry_in_toc:
            yield f'{markdown_entry}[{num_entry + title}]({nb_name})\n'
        else:
            yield f'{markdown_entry}[{title}]({nb_name})\n'
 

def print_contents(app_to_notes_path='.', 
                   show_full_entry_in_toc=True):
    print('\n'.join(yield_contents(app_to_notes_path, 
                                   show_full_entry_in_toc)))


def get_contents(app_to_notes_path='.', show_full_entry_in_toc=True):
    """
    Returns a string with the 'Table of Contents' constructed 
    from the collection of notebooks in the 'app_to_notes_path' given
    as argument.
    """

    contents = ""
    for item in yield_contents(app_to_notes_path, show_full_entry_in_toc):
        contents += item + "\n"
    
    return contents

def add_contents(toc_nb_name, app_to_notes_path='.',
                 show_full_entry_in_toc=True):
    # error handling
    assert(type(app_to_notes_path)==str), "Argument 'app_to_notes_path' should be a string"
    assert(type(toc_nb_name)==str), "Argument 'toc_nb_name' should be a string"

    contents = TOC_MARKER + "\n\n"
    for item in yield_contents(app_to_notes_path, show_full_entry_in_toc):
        contents += item + "\n"

    toc_nb_file = os.path.join(app_to_notes_path, toc_nb_name)

    toc_nb = nbformat.read(toc_nb_file, as_version=4)

    toc_cell_found = False
    for cell in toc_nb.cells:
        if is_marker_cell(TOC_MARKER, cell):
            cell.source = contents
            toc_cell_found = True
            
    if toc_cell_found:
        nbformat.write(toc_nb, toc_nb_file)
        print(f'- Table of contents updated in {toc_nb_name}')
    else:
        print(f'* No markdown cell starting with {TOC_MARKER} found in {toc_nb_name}')
        print("- inserting table of contents in {0}".format(toc_nb_name))
        if toc_nb.cells and is_marker_cell(NAVIGATOR_MARKER, toc_nb.cells[-1]):
            toc_nb.cells.insert(-1, new_markdown_cell(source=contents))
        else:
            toc_nb.cells.append(new_markdown_cell(source=contents))

    nbformat.write(toc_nb, toc_nb_file)

def add_headers(header, app_to_notes_path='.'):
    for nb_name in indexed_notebooks(app_to_notes_path):
        nb_file = os.path.join(app_to_notes_path, nb_name)
        nb = nbformat.read(nb_file, as_version=4)

        if nb.cells and is_marker_cell(HEADER_MARKER, nb.cells[0]):    
            print('- updating header for {0}'.format(nb_name))
            nb.cells[0].source = HEADER_MARKER + '\n' + header
        else:
            print('- inserting header for {0}'.format(nb_name))
            nb.cells.insert(0, new_markdown_cell(HEADER_MARKER + '\n' + header))
        nbformat.write(nb, nb_file)

def prev_this_next(it):
    a, b, c = itertools.tee(it,3)
    next(c)
    return zip(itertools.chain([None], a), b, itertools.chain(c, [None]))

def get_navigator_entries(core_navigators = [], app_to_notes_path='.', 
                          user = '', repository = '', 
                          branch = '',
                          github_nb_dir = '', 
                          github_io_slides_dir = '',
                          show_full_entry_in_nav = True):

    PREV_TEMPLATE = "[<- {title}]({url}) "
    CENTER_TEMPLATE = "| [{title}]({url}) "
    NEXT_TEMPLATE = "| [{title} ->]({url})"

    COLAB_LINK = """
<a href="https://colab.research.google.com/github/{user}/{repository}/blob/{branch}/{github_nb_dir}/{notebook_filename}"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open and Execute in Google Colaboratory"></a>
"""
    BINDER_LINK = """
<a href="https://mybinder.org/v2/gh/{user}/{repository}/{branch}?filepath={github_nb_dir}/{notebook_filename}"><img align="left" src="https://mybinder.org/badge.svg" alt="Open in binder" title="Open and Execute in Binder"></a>
"""
    SLIDES_LINK = """
<a href="https://{user}.github.io/{repository}/{github_io_slides_dir}/{slides_filename}"><img align="left" src="https://rmsrosa.github.io/nbbinder/badges/slides_badge.svg" alt="Open slides" title="Open and View Slides"></a>
"""

    for prev_nb, this_nb, next_nb in prev_this_next(indexed_notebooks(app_to_notes_path)):
        navbar = ""
        if prev_nb:
            entry = get_notebook_entry(prev_nb, app_to_notes_path, 
                                       show_full_entry_in_nav)
            navbar += PREV_TEMPLATE.format(title=entry, url=prev_nb)

        for center_nb in core_navigators:
            entry = get_notebook_entry(center_nb, app_to_notes_path, 
                                       show_full_entry_in_nav)
            navbar += CENTER_TEMPLATE.format(title=entry, url=center_nb)

        if next_nb:
            entry = get_notebook_entry(next_nb, app_to_notes_path, 
                                       show_full_entry_in_nav)
            navbar += NEXT_TEMPLATE.format(title=entry, url=next_nb)

        this_colab_link = COLAB_LINK.format(user=user,
            repository=repository, 
            branch=branch, github_nb_dir=github_nb_dir, 
            notebook_filename=os.path.basename(this_nb))
        this_binder_link = BINDER_LINK.format(user=user,
            repository=repository, 
            branch=branch, github_nb_dir=github_nb_dir, 
            notebook_filename=os.path.basename(this_nb))
        this_slide_link = SLIDES_LINK.format(user=user, 
            repository=repository,
            github_io_slides_dir=github_io_slides_dir,
            slides_filename=os.path.basename(this_nb.replace('.ipynb',
                                                             '.slides.html')))
            
        yield os.path.join(app_to_notes_path, this_nb), navbar, this_colab_link, this_binder_link, this_slide_link

def add_navigators(core_navigators=[], app_to_notes_path='.', 
                   user = '', repository = '', branch = '', 
                   github_nb_dir = '',
                   github_io_slides_dir = '',
                   show_colab=False, show_binder=False, 
                   show_slides=False,
                   show_full_entry_in_nav=True):
    for nb_file, navbar, this_colab_link, this_binder_link, this_slide_link in get_navigator_entries(core_navigators, app_to_notes_path, 
                          user, repository, branch, 
                          github_nb_dir,
                          github_io_slides_dir, 
                          show_full_entry_in_nav):
        nb = nbformat.read(nb_file, as_version=4)
        nb_name = os.path.basename(nb_file)

        navbar_top = navbar_bottom = NAVIGATOR_MARKER + "\n"
        navbar_bottom = NAVIGATOR_MARKER + "\n\n---\n" + navbar
            
        if show_colab and show_binder:
            navbar_top += this_colab_link + "&nbsp;" + this_binder_link + "&nbsp;\n"
            navbar_bottom += "\n" + this_colab_link + this_binder_link + "&nbsp;" 
        elif show_colab:
            navbar_top += this_colab_link + "&nbsp;\n"
            navbar_bottom += "\n" + this_colab_link
        elif show_binder:
            navbar_top += this_binder_link + "&nbsp;\n" 
            navbar_bottom += "\n" + this_binder_link

        navbar_top = navbar_bottom = NAVIGATOR_MARKER + "\n"
        navbar_bottom = NAVIGATOR_MARKER + "\n\n---\n" + navbar

        if show_colab or show_binder or show_slides:
            navbar_bottom += "\n"

        if show_colab:
            navbar_top += this_colab_link + "&nbsp;"
            navbar_bottom += this_colab_link

        if show_binder:
            navbar_top += this_binder_link + "&nbsp;"
            navbar_bottom += this_binder_link

        if show_slides:
            navbar_top += this_slide_link + "&nbsp;"
            navbar_bottom += this_slide_link

        if show_colab or show_binder or show_slides:
            navbar_top += "\n"
            navbar_bottom += "&nbsp;"

        navbar_top += "\n" + navbar + "\n\n---\n"

        if len(nb.cells) > 1 and is_marker_cell(NAVIGATOR_MARKER, nb.cells[1]):         
            print("- updating navbar for {0}".format(nb_name))
            nb.cells[1].source = navbar_top
        else:
            print("- inserting navbar for {0}".format(nb_name))
            nb.cells.insert(1, new_markdown_cell(source=navbar_top))

        if len(nb.cells)>2 and is_marker_cell(NAVIGATOR_MARKER, nb.cells[-1]):
            nb.cells[-1].source = navbar_bottom
        else:
            nb.cells.append(new_markdown_cell(source=navbar_bottom))
        nbformat.write(nb, nb_file)

def bind(toc_nb_name, header, core_navigators,
         app_to_notes_path='.', 
         restructure_notebooks=False,
         user='', repository='', branch='', 
         github_nb_dir='',
         github_io_slides_dir='',
         show_colab=False, show_binder=False, 
         show_slides=False,
         show_full_entry_in_toc=True,
         show_full_entry_in_nav=True):

    if restructure_notebooks:
        restructure(app_to_notes_path)

    add_contents(toc_nb_name=toc_nb_name, 
                 app_to_notes_path=app_to_notes_path,
                 show_full_entry_in_toc=show_full_entry_in_toc)

    add_headers(header = header, app_to_notes_path = app_to_notes_path)

    add_navigators(core_navigators=core_navigators,
                   app_to_notes_path=app_to_notes_path, 
                   user=user, 
                   repository=repository, branch=branch, 
                   github_nb_dir=github_nb_dir,
                   github_io_slides_dir=github_io_slides_dir,
                   show_colab=show_colab, 
                   show_binder=show_binder,
                   show_slides=show_slides,
                   show_full_entry_in_nav=show_full_entry_in_nav)

def bind_from_configfile(config_file):
    with open(config_file, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    if 'directory' in config:
        app_to_notes_path = config['directory']['app_to_notes_path']
    else:
        app_to_notes_path = '.'

    if 'book' in config:
        bind(**config['book'], 
             app_to_notes_path=app_to_notes_path)
    else:
        if 'restructure_notebooks' in config:
            if config['restructure_notebooks']:
                restructure(app_to_notes_path)

        if 'contents' in config:
            add_contents(**config['contents'], 
                app_to_notes_path=app_to_notes_path)

        if 'header' in config:
            add_headers(**config['header'], 
                app_to_notes_path=app_to_notes_path)
        else:
            remove_marker_cell(HEADER_MARKER, app_to_notes_path)

        if 'navigator' in config:
            add_navigators(**config['navigator'], 
                app_to_notes_path=app_to_notes_path)
        else:
            remove_marker_cell(NAVIGATOR_MARKER, app_to_notes_path)

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '--help' or sys.argv[1] == '-h':
        print("\n Run the script with a configuration file as argument, e.g.")
        print("\n   ./nbbinder.py config.yml")
        print("\nFor the documentation, type 'pydoc3 nbbinder.py'.\n")
    else:
        try:
            bind_from_configfile(sys.argv[1])
        except NotImplementedError:
            print('provided argument is not a file or not a properly formated yaml configuration file.')
