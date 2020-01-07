
#!/anaconda3/envs/nbbinder/bin/python
# -*- coding: utf-8 -*-
'''
Basic Module for the test files
'''

import os
import logging
import shutil

import nbformat
from nbformat.v4.nbbase import new_markdown_cell

from faker import Faker

from context import nbbinder as nbb

# Logging level
logging.basicConfig(level=logging.WARNING)


def change_to_file_dir():
    """
    Change current directory to that where this file resides.
    """
    os.chdir(os.path.dirname(__file__))
    logging.info("# Directory changed to '{arg}'",
                 arg=os.path.dirname(__file__))


def get_source_path(path):
    """
    Returns the path preprended with the source directory `nb_source`.
    """
    return os.path.join('nb_source', path)


def create_build_dir(build_dir):
    """
    Creates the build directory `build_dir`.
    """
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)
    os.mkdir(build_dir)
    logging.info("Build directory '{arg}' created.", arg=build_dir)


def get_build_path(build_dir, path: str = '.'):
    """
    Returns the path preprended with the given build directory.
    """
    return os.path.join(build_dir, path)


def create_notebooks(path_to_notes, nb_filenames):
    """
    Creates Jupyter notebook files from a list of filenames.
    """
    assert(isinstance(path_to_notes, str)), "Argument `path_to_notes` \
           should be a string"

    if os.path.isdir(path_to_notes):
        for file in os.listdir(path_to_notes):
            os.remove(os.path.join(path_to_notes, file))
    else:
        os.mkdir(path_to_notes)

    fake = Faker()
    fake.seed_instance(1234)

    for nb_filename in nb_filenames:
        notebook = nbformat.v4.new_notebook()
        nb_reg = nbb.REG_INSERT.match(nb_filename)
        title_md = '# ' + \
            nb_reg.group(5).replace('_', ' ').replace('+u003f', '?')
        notebook.cells.insert(0, new_markdown_cell(title_md))
        notebook.cells.insert(1, new_markdown_cell(source=fake.text(),
                                                   metadata=nbb.SLIDE_SHOW))
        notebook.cells.insert(2, new_markdown_cell(source=fake.text(),
                                                   metadata=nbb.SLIDE_SHOW))
        notebook.cells.insert(3, new_markdown_cell(source=fake.text(),
                                                   metadata=nbb.SLIDE_SHOW))
        nbformat.write(notebook, os.path.join(path_to_notes, nb_filename))

    logging.info("\n# Notebooks created in {arg}", arg=path_to_notes)


def bind_test(source_path, build_path, config_file):
    """
    Binds the notebooks.

    If different, copies the notebook files from the `source_path` to
    the `build_path` and binds the notebooks in `build_path` according
    to the configuration file `config_file`.
    """
    if build_path != source_path:
        logging.info("\n# Copying source notebooks to build directory")

        shutil.copytree(source_path, build_path)

    logging.info("\n# Binding the notebooks in {arg1} with '{arg2}'",
                 arg1=source_path, arg2=config_file)

    nbb.bind(config_file)
