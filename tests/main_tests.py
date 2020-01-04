#!/anaconda3/envs/nbbinder/bin/python
# -*- coding: utf-8 -*-
'''
Main Binder test
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

# Build dir
BUILD_DIR = 'nb_builds'

def get_source_path(path):
    return os.path.join('nb_source', path)

def create_build_dir():
    if os.path.isdir(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.mkdir(BUILD_DIR)
    logging.info("Build directory '{}' created.".format(BUILD_DIR))

def get_build_path(path: str='.'):
    return os.path.join(BUILD_DIR, path)

def get_build_path(path: str='.'):
    return os.path.join('nb_builds', path)

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

if __name__ == '__main__':

    logging.info("# Changing to directory '{}'".format(
        os.path.dirname(__file__)))
    os.chdir(os.path.dirname(__file__))

    logging.info("# Creating build directory '{}'.".format(BUILD_DIR))
    create_build_dir()

    nb_alice = [
        "00.00-Alice's_Adventures_in_Wonderland.ipynb",
        "01.00-Down_the_Rabbit-Hole.ipynb",
        "02.00-The_Pool_of_Tears.ipynb",
        "03.00-A_Caucus-Race_and_a_Long_Tale.ipynb",
        "04.00-The_Rabbit_Sends_in_a_Little_Bill.ipynb",
        "05.00-Advice_from_a_Caterpillar.ipynb",
        "06.00-Pig_and_Pepper.ipynb",
        "07.00-A_Mad_Tea-Party.ipynb",
        "08.00-The_Queen's_Croquet-Ground.ipynb",
        "09.00-The_Mock_Turtle's_Story.ipynb",
        "10.00-The_Lobster_Quadrille.ipynb",
        "11.00-Who_Stole_the_Tarts+u003f.ipynb",
        "12.00-Alice's_Evidence.ipynb"
    ]

    logging.info("# Creating notebooks in {} ...".format(os.path.join(os.path.dirname(__file__), 'nb_alice')))
    create_notebooks(get_build_path('nb_alice'), nb_alice)
    logging.info('... notebooks created')
    logging.info("\n# Reindexing the notebooks in {}".format(os.path.join(os.path.dirname(__file__), 'nb_alice')))
    nbb.reindex(get_build_path('nb_alice'))

    logging.info("\n# Binding 'nb_alice' notebooks with parameters")
    nbb.bind(path_to_notes=get_build_path('nb_alice'),
        toc_nb_name="00.00-Alice's_Adventures_in_Wonderland.ipynb",
        show_index_in_toc=True,
        header="[*NBBinder test on a collection of notebooks named after the chapters of 'Alice's Adventures in Wonderland'*](https://github.com/rmsrosa/nbbinder)",
        core_navigators=[
            "00.00-Alice's_Adventures_in_Wonderland.ipynb"
            ],
        user='rmsrosa',
        repository='nbbinder',
        branch='master',
        github_nb_dir=os.path.join('tests', get_build_path('nb_alice')),
        show_colab=True,
        show_binder=True,
        show_index_in_nav=False)

    logging.info("\n# Binding 'nb_alice' notebooks with config file 'config_nb_alice.yml'")
    nbb.bind(get_source_path('config_nb_alice.yml'))

    nb_grammar = [
        '00.00-Front_Page.ipynb',
        '01.00-Introduction.ipynb',
        '02.00-Project_Requirements.ipynb',
        '03.00-The_History_of_Grammar.ipynb',
        '04.00-Parts_of_Speech.ipynb',
        '04.01-Nouns.ipynb',
        '04.02-Verbs.ipynb',
        '04.03-Adjectives.ipynb',
        '04.04-Adverbs.ipynb',
        '05.00-Sentences.ipynb',
        '05.01-Complex_Sentences.ipynb',
        '05.02-Compound_Sentences.ipynb',
        '06.00-Paragraphs.ipynb',
        '06.01-Descriptive.ipynb',
        '06.02-Expository.ipynb',
        '06.03-Narrative.ipynb',
        '06.04-Persuasive.ipynb',
        '07.00-Conclusion.ipynb',
        'AA.00-Appendix.ipynb',
        'BA.00-Glossary.ipynb',
        'BB.00-Bibliography.ipynb',
        'BC.00-Index.ipynb'
    ]

    logging.info("\n# Creating notebooks in {}".format(os.path.join(os.path.dirname(__file__), 'nb_grammar')))
    create_notebooks(get_build_path('nb_grammar'), nb_grammar)
    logging.info("\n# Reindexing the notebooks in {}".format(os.path.join(os.path.dirname(__file__), get_build_path('nb_grammar'))))
    nbb.reindex(get_build_path('nb_grammar'))

    logging.info("\n# Creating notebooks in {}".format(os.path.join(os.path.dirname(__file__), 'nb_grammar_bound')))
    create_notebooks(get_build_path('nb_grammar_bound'), nb_grammar)
    logging.info("\n# Binding the notebooks in {} with 'config_nb_grammar.yml'".format(os.path.join(os.path.dirname(__file__), get_build_path('nb_grammar_bound'))))
    nbb.bind(get_source_path('config_nb_grammar.yml'))

    logging.info("\n# Binding the notebooks in {} with 'config_nb_grammar_no_header.yml'".format(os.path.join(os.path.dirname(__file__), get_build_path('nb_grammar_bound'))))
    nbb.bind(get_source_path('config_nb_grammar_no_header.yml'))

    logging.info("\n# Binding the notebooks in {} with 'config_nb_grammar_reindex.yml'".format(os.path.join(os.path.dirname(__file__), get_build_path('nb_grammar_bound'))))
    nbb.bind(get_source_path('config_nb_grammar_reindex.yml'))

    logging.info("\n# Binding the notebooks in {} with 'nbb.bind()'".format(os.path.join(os.path.dirname(__file__), get_build_path('nb_grammar_bound'))))
    nbb.bind(path_to_notes=get_build_path('nb_grammar_bound'),
        insert=True, tighten=True,
        toc_nb_name='00.00-Front_Page.ipynb',
        toc_title='Table of Contents',
        show_index_in_toc=True,
        header="[*Test Grammar for the NBBinder module*](https://github.com/rmsrosa/nbbinder)",
        core_navigators=['00.00-Front_Page.ipynb', 
        'BB.00-Bibliography.ipynb'],
        show_index_in_nav=False)

    nb_grammar_insert = [
        '00.00-Front_Page.ipynb',
        '01.00-Introduction.ipynb',
        '01a.00-Project_Requirements.ipynb',
        '01b.00-The_History_of_Grammar.ipynb',
        '02.00-Parts_of_Speech.ipynb',
        '04.01-Nouns.ipynb',
        '04.01i-Verbs.ipynb',
        '04.02-Adjectives.ipynb',
        '04.03-Adverbs.ipynb',
        '05.00-Sentences.ipynb',
        '05.00i-Complex_Sentences.ipynb',
        '05.01-Compound_Sentences.ipynb',
        '06.00-Paragraphs.ipynb',
        '06.01-Descriptive.ipynb',
        '06.01i-Expository.ipynb',
        '06.01j-Narrative.ipynb',
        '06.02-Persuasive.ipynb',
        '07.00-Conclusion.ipynb',
        'AA.00-Appendix.ipynb',
        'BA.00-Glossary.ipynb',
        'BAi.00-Bibliography.ipynb',
        'BB.00-Index.ipynb'
    ]

    logging.info("\n# Creating notebooks in {}".format(os.path.join(os.path.dirname(__file__), get_build_path('nb_grammar_insert'))))
    create_notebooks(get_build_path('nb_grammar_insert'), nb_grammar_insert)
    logging.info("\n# Reindexing the notebooks in {}".format(os.path.join(os.path.dirname(__file__), get_build_path('nb_grammar_insert'))))
    nbb.reindex(get_build_path('nb_grammar_insert'), insert=True)

    nb_grammar_tighten = [
        '00.00-Front_Page.ipynb',
        '02.00-Introduction.ipynb',
        '04.00-Project_Requirements.ipynb',
        '05.00-The_History_of_Grammar.ipynb',
        '06.00-Parts_of_Speech.ipynb',
        '06.02-Nouns.ipynb',
        '06.03-Verbs.ipynb',
        '06.05-Adjectives.ipynb',
        '06.08-Adverbs.ipynb',
        '08.00-Sentences.ipynb',
        '08.01-Complex_Sentences.ipynb',
        '08.03-Compound_Sentences.ipynb',
        '09.00-Paragraphs.ipynb',
        '09.01-Descriptive.ipynb',
        '09.02-Expository.ipynb',
        '09.03-Narrative.ipynb',
        '09.04-Persuasive.ipynb',
        '11.00-Conclusion.ipynb',
        'AB.00-Appendix.ipynb',
        'BA.00-Glossary.ipynb',
        'BC.02-Bibliography.ipynb',
        'BC.04-Index.ipynb'
    ]

    logging.info("\n# Creating notebooks in {}".format(os.path.join(os.path.dirname(__file__), get_build_path('nb_grammar_tighten'))))
    create_notebooks(get_build_path('nb_grammar_tighten'), nb_grammar_tighten)
    logging.info("\n# Reindexing the notebooks in {}".format(os.path.join(os.path.dirname(__file__), get_build_path('nb_grammar_tighten'))))
    nbb.reindex(get_build_path('nb_grammar_tighten'), tighten=True)

    logging.info("\n# Copying water source notebooks to build directory")
    shutil.copytree(get_source_path('nb_water'), get_build_path('nb_water'))
    logging.info("\n# Binding the notebooks in {} with 'config_nb_water.yml'".format(os.path.join(os.path.dirname(__file__), get_build_path('nb_water'))))
    nbb.bind(get_source_path('config_nb_water.yml'))