#!/anaconda3/envs/nbbinder/bin/python
# -*- coding: utf-8 -*-
'''
Basic Module for the NBBinder test files
'''

import os
import logging
import shutil

import nbformat
from nbformat.v4.nbbase import new_markdown_cell

from faker import Faker

from context import nbbinder as nbb

# Logging level
#logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# pylint: disable=E1101

def change_to_file_dir():
    """
    Change current directory to that where this file resides.
    """
    os.chdir(os.path.dirname(__file__))
    logger.info("# Directory changed to '%s'",
                 os.path.dirname(__file__))


def create_build_dir(build_dir):
    """
    Creates the build directory `build_dir`.
    """
    if os.path.isdir(build_dir):
        shutil.rmtree(build_dir)
    os.mkdir(build_dir)
    logger.info("Build directory '%s' created.", build_dir)


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
        nb_reg = nbb.REG_INS.match(nb_filename)
        title_md = '# ' + \
            nb_reg.group(6).replace('_', ' ').replace('+u003f', '?')
        notebook.cells.insert(0, new_markdown_cell(title_md))
        notebook.cells.insert(1, new_markdown_cell(source=fake.text(),
                                                   metadata=nbb.SLIDE_SHOW))
        notebook.cells.insert(2, new_markdown_cell(source=fake.text(),
                                                   metadata=nbb.SLIDE_SHOW))
        notebook.cells.insert(3, new_markdown_cell(source=fake.text(),
                                                   metadata=nbb.SLIDE_SHOW))
        nbformat.write(notebook, os.path.join(path_to_notes, nb_filename))

    logger.info("\n# Notebooks created in '%s'", path_to_notes)


def bind_test(source_path, build_path, config_file):
    """
    Binds the notebooks.

    If different, copies the notebook files from the `source_path` to
    the `build_path` and binds the notebooks in `build_path` according
    to the configuration file `config_file`.
    """
    if build_path != source_path:
        logger.info("\n# Copying source notebooks to build directory")

        shutil.copytree(source_path, build_path)

    logger.info("\n# Binding the notebooks in '%s' with '%s'",
                 source_path, config_file)

    nbb.bind(config_file)
