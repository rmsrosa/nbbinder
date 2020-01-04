
#!/anaconda3/envs/nbbinder/bin/python
# -*- coding: utf-8 -*-
'''
Basic Module for the test files
'''

import os
import logging

import shutil

from faker import Faker

import nbformat
from nbformat.v4.nbbase import new_markdown_cell

from context import nbbinder as nbb

# Logging level
logging.basicConfig(level=logging.WARNING)

def get_source_path(path):
    return os.path.join('nb_source', path)

def create_build_dir():
    if os.path.isdir(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.mkdir(BUILD_DIR)
    logging.info("Build directory {} created.".format(BUILD_DIR))

def get_build_path(path: str='.'):
    return os.path.join(BUILD_DIR, path)

def bind_test(source_path, build_path, config_file):

    if build_path != source_path:
        logging.info("\n# Copying source notebooks to build directory")

        shutil.copytree(source_path, build_path)

    logging.info("\n# Binding the notebooks in {} with '{}'".format(
        source_path, config_file))

    nbb.bind(config_file)

def create_notebooks(path_to_notes, nb_filenames):

    assert(type(path_to_notes)==str), "Argument `path_to_notes` should be a string"

    if os.path.isdir(path_to_notes):
        for f in os.listdir(path_to_notes):
            os.remove(os.path.join(path_to_notes,f))
    else:
        os.mkdir(path_to_notes)

    fake = Faker()
    fake.seed_instance(1234)

    for nb_filename in nb_filenames:
        nb = nbformat.v4.new_notebook()
        nb_reg = nbb.REG_INSERT.match(nb_filename)
        nb.cells.insert(0, new_markdown_cell('# ' + nb_reg.group(5).replace('_', ' ').replace('+u003f','?')))
        nb.cells.insert(1, new_markdown_cell(source=fake.text(), 
            metadata=nbb.SLIDE_SHOW))
        nb.cells.insert(2, new_markdown_cell(source=fake.text(),
            metadata=nbb.SLIDE_SHOW))
        nb.cells.insert(3, new_markdown_cell(source=fake.text(),
            metadata=nbb.SLIDE_SHOW))
        nbformat.write(nb, os.path.join(path_to_notes, nb_filename))