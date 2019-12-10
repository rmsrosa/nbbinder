#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Notebook Binder test
'''

import os
import re

import nbformat
from nbformat.v4.nbbase import new_markdown_cell

from context import nbbinder as nbb

def create_notebooks(nb_dir, nb_filenames):

    if os.path.isdir(nb_dir):
        for f in os.listdir(nb_dir):
            os.remove(os.path.join(nb_dir,f))
    else:
        os.mkdir(nb_dir)

    for nb_filename in nb_filenames:
        nb = nbformat.v4.new_notebook()
        nb_reg = nbb.nbbinder.REG_STAR.match(nb_filename)
        nb.cells.insert(0, new_markdown_cell('# ' + nb_reg.group(5).replace('_', ' ').replace('+u003f','?')))
        if nb_reg.group(1) == '00':
            text = "That's all for this part of the Front Matter"
        elif nb_reg.group(1)[0] == 'A':
            text = "That's all for this part of the Appendix"
        elif nb_reg.group(1)[0] == 'B':
            text = "That's all for this part of the End Matter"
        else:
            text = "That's all for this Section"
        nb.cells.insert(1, new_markdown_cell(text))
        nbformat.write(nb, os.path.join(nb_dir, nb_filename))

if __name__ == '__main__':

    print("# Changing to directory {}".format(os.path.dirname(__file__)))
    os.chdir(os.path.dirname(__file__))

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

    print("# Creating notebooks in {} ...".format(os.path.join(os.path.dirname(__file__), 'nb_alice')))
    create_notebooks('nb_alice', nb_alice)
    print('... notebooks created')
    print("\n# Reestructuring the notebooks in {}".format(os.path.join(os.path.dirname(__file__), 'nb_alice')))
    nbb.restructure('nb_alice')

    print("\n# Binding notebooks with config file 'config_nb_alice.yml'")
    nbb.bind('config_nb_alice.yml')

    print("\n# Binding notebooks with config file 'config_nb_alice.yml'")
    nbb.bind(path_to_notes="nb_alice",
        toc_nb_name="00.00-Alice's_Adventures_in_Wonderland.ipynb",
        show_full_entry_in_toc=True,
        header="[*NBBinder test on a collection of notebooks named after the chapters of 'Alice's Adventures in Wonderland'*](https://github.com/rmsrosa/nbbinder)",
        core_navigators=[
            "00.00-Alice's_Adventures_in_Wonderland.ipynb"
            ],
        user='rmsrosa',
        repository='nbbinder',
        branch='master',
        github_nb_dir='tests/nb_alice',
        show_colab=True,
        show_binder=True,
        show_full_entry_in_nav=False)

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
        'BA.00-Index.ipynb'
    ]

    print("\n# Creating notebooks in {}".format(os.path.join(os.path.dirname(__file__), 'nb_grammar')))
    create_notebooks('nb_grammar', nb_grammar)
    print("\n# Reestructuring the notebooks in {}".format(os.path.join(os.path.dirname(__file__), 'nb_grammar')))
    nbb.restructure('nb_grammar')

    print("\n# Creating notebooks in {}".format(os.path.join(os.path.dirname(__file__), 'nb_grammar_bound')))
    create_notebooks('nb_grammar_bound', nb_grammar)
    print("\n# Binding the notebooks in {} with 'config_nb_grammar.yml'".format(os.path.join(os.path.dirname(__file__), 'nb_grammar_bound')))
    nbb.bind('config_nb_grammar.yml')

    print("\n# Binding the notebooks in {} with 'config_nb_grammar_no_header.yml'".format(os.path.join(os.path.dirname(__file__), 'nb_grammar_bound')))
    nbb.bind('config_nb_grammar_book.yml')

    print("\n# Binding the notebooks in {} with 'config_nb_grammar_book.yml'".format(os.path.join(os.path.dirname(__file__), 'nb_grammar_bound')))
    nbb.bind('config_nb_grammar_no_header.yml')

    print("\n# Binding the notebooks in {} with 'nbb.bind()'".format(os.path.join(os.path.dirname(__file__), 'nb_grammar_bound')))
    nbb.bind(path_to_notes='nb_grammar_bound',
            toc_nb_name='00.00-Front_Page.ipynb',
            show_full_entry_in_toc=True,
            header="[*Test Grammar for the NBBinder module*](https://github.com/rmsrosa/nbbinder)",
            core_navigators=['00.00-Front_Page.ipynb', 
            'BB.00-Bibliography.ipynb'],
            show_full_entry_in_nav=False)

    nb_grammar_missing = [
        '00.00-Front_Page.ipynb',
        '01.00-Introduction.ipynb',
        '01a.00-Project_Requirements.ipynb',
        '01b.00-The_History_of_Grammar.ipynb',
        '02.00-Parts_of_Speech.ipynb',
        '04.01-Nouns.ipynb',
        '04.01i-Verbs.ipynb',
        '04.02j-Adjectives.ipynb',
        '04.03-Adverbs.ipynb',
        '05.00-Sentences.ipynb',
        '05.00i-Complex_Sentences.ipynb',
        '05.01-Compound_Sentences.ipynb',
        '06.00-Paragraphs.ipynb',
        '06.01-Descriptive.ipynb',
        '06.01i-Expository.ipynb',
        '06.02ii-Narrative.ipynb',
        '06.04-Persuasive.ipynb',
        '07.00-Conclusion.ipynb',
        'AA.00-Appendix.ipynb',
        'BA.00-Glossary.ipynb',
        'BBi.00-Bibliography.ipynb',
        'BB.00-Index.ipynb'
    ]

    print("\n# Creating notebooks in {}".format(os.path.join(os.path.dirname(__file__), 'nb_grammar_missing')))
    create_notebooks('nb_grammar_missing', nb_grammar_missing)
    print("\n# Reestructuring the notebooks in {}".format(os.path.join(os.path.dirname(__file__), 'nb_grammar_missing')))    
    nbb.restructure('nb_grammar_missing')