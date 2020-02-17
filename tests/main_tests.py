#!/anaconda3/envs/nbbinder/bin/python
# -*- coding: utf-8 -*-
'''
Main NBBinder test
'''

import os
import logging

import basetest as bt

from context import nbbinder as nbb

# Logging level
logging.basicConfig(level=logging.WARNING)

# bt.logger.setLevel(logging.INFO)
# nbb.logger.setLevel(logging.INFO)

# Directories
BUILD_DIR = 'nb_builds'
SOURCE_DIR = 'nb_source'

if __name__ == '__main__':

    bt.change_to_file_dir()

    bt.create_build_dir(BUILD_DIR)

    # Tests with nb_alice

    NB_ALICE = [
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

    logging.info("# Creating notebooks in %s ...",
                 os.path.join(os.path.dirname(__file__),
                              BUILD_DIR, 'nb_alice'))
    bt.create_notebooks(os.path.join(BUILD_DIR, 'nb_alice'), NB_ALICE)
    logging.info('... notebooks created')
    logging.info("\n# Reindexing the notebooks in %s",
                 os.path.join(os.path.dirname(__file__),
                              BUILD_DIR, 'nb_alice'))
    nbb.reindex(os.path.join(BUILD_DIR, 'nb_alice'))

    logging.info("\n# Binding 'nb_alice' notebooks with parameters")

    nbb.bind(
        path_to_notes=os.path.join(BUILD_DIR, 'nb_alice'),
        contents={
            'toc_nb_name': "00.00-Alice's_Adventures_in_Wonderland.ipynb",
            'show_index_in_toc': True
            },
        header="NBBinder test with 'Alice's Adventures in Wonderland'",
        navigators={
            'core_navigators':
                ["00.00-Alice's_Adventures_in_Wonderland.ipynb"],
            'show_index_in_nav': False
            }
        )

    bt.bind_test(os.path.join(BUILD_DIR, 'nb_alice'),
                 os.path.join(BUILD_DIR, 'nb_alice'),
                 os.path.join(SOURCE_DIR, 'config_nb_alice.yml'))

    # Tests with nb_grammar

    NB_GRAMMAR = [
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
        'A0.00-Appendix.ipynb',
        'BA.00-Glossary.ipynb',
        'BB.00-Bibliography.ipynb',
        'BC.00-Index.ipynb'
    ]

    logging.info("\n# Creating notebooks in %s",
                 os.path.join(os.path.dirname(__file__),
                              BUILD_DIR, 'nb_grammar'))
    bt.create_notebooks(os.path.join(BUILD_DIR, 'nb_grammar'), NB_GRAMMAR)
    logging.info("\n# Reindexing the notebooks in %s",
                 os.path.join(os.path.dirname(__file__),
                              BUILD_DIR, 'nb_grammar'))
    nbb.reindex(os.path.join(BUILD_DIR, 'nb_grammar'))

    bt.create_notebooks(os.path.join(BUILD_DIR, 'nb_grammar_bound'),
                        NB_GRAMMAR)

    bt.bind_test(os.path.join(BUILD_DIR, 'nb_grammar_bound'),
                 os.path.join(BUILD_DIR, 'nb_grammar_bound'),
                 os.path.join(SOURCE_DIR, 'config_nb_grammar.yml'))

    bt.bind_test(os.path.join(BUILD_DIR, 'nb_grammar_bound'),
                 os.path.join(BUILD_DIR, 'nb_grammar_bound'),
                 os.path.join(SOURCE_DIR, 'config_nb_grammar_no_header.yml'))

    bt.bind_test(os.path.join(BUILD_DIR, 'nb_grammar_bound'),
                 os.path.join(BUILD_DIR, 'nb_grammar_bound'),
                 os.path.join(SOURCE_DIR, 'config_nb_grammar_reindex.yml'))

    logging.info("\n# Binding the notebooks in %s with 'nbb.bind()'",
                 os.path.join(os.path.dirname(__file__),
                              BUILD_DIR, 'nb_grammar_bound'))

    nbb.bind(
        path_to_notes=os.path.join(BUILD_DIR, 'nb_grammar_bound'),
        reindexing={
            'insert': True,
            'tighten': True
        },
        contents={
            'toc_nb_name': '00.00-Front_Page.ipynb',
            'toc_title': 'Table of Contents',
            'show_index_in_toc': True
        },
        header="NB Grammar Test for the NBBinder module",
        navigators={
            'core_navigators': [
                '00.00-Front_Page.ipynb',
                'BB.00-Bibliography.ipynb'
            ],
            'show_index_in_nav': False
        },
        badges=[
            {
                'title': 'View in NBViewer',
                'url': 'https://nbviewer.jupyter.org/github/rmsrosa/\
nbbinder/blob/master/tests/nb_builds/nb_alice',
                'label': 'view in',
                'message': 'nbviewer',
                'color': 'orange'},
            {
                'title': 'View Markdown',
                'url': 'https://github.com/rmsrosa/nbbinder/blob/master/\
tests/nb_builds/nb_grammar_md',
                'extension': '.md',
                'label': 'view',
                'message': 'markdown',
                'color': 'blueviolet'
            }
        ]
        )

    # Tests with nb_grammar_insert

    NB_GRAMMAR_INSERT = [
        '00.00-Front_Page.ipynb',
        '01.00-Introduction.ipynb',
        '02&a.00-Project_Requirements.ipynb',
        '02&b.00-The_History_of_Grammar.ipynb',
        '02.00-Parts_of_Speech.ipynb',
        '04.01&-Nouns.ipynb',
        '04.01-Verbs.ipynb',
        '04.02-Adjectives.ipynb',
        '04.03-Adverbs.ipynb',
        '05.00-Sentences.ipynb',
        '05.01&-Complex_Sentences.ipynb',
        '05.01-Compound_Sentences.ipynb',
        '06.00-Paragraphs.ipynb',
        '06.01-Descriptive.ipynb',
        '06.02&a-Expository.ipynb',
        '06.02&b-Narrative.ipynb',
        '06.02-Persuasive.ipynb',
        '07.00-Conclusion.ipynb',
        'AA.00-Appendix.ipynb',
        'BA.00-Glossary.ipynb',
        'BB&.00-Bibliography.ipynb',
        'BB.00-Index.ipynb'
    ]

    logging.info("\n# Creating notebooks in %s",
                 os.path.join(os.path.dirname(__file__),
                              BUILD_DIR, 'nb_grammar_insert'))
    bt.create_notebooks(os.path.join(BUILD_DIR, 'nb_grammar_insert'),
                        NB_GRAMMAR_INSERT)
    logging.info("\n# Reindexing the notebooks in %s",
                 os.path.join(os.path.dirname(__file__),
                              BUILD_DIR, 'nb_grammar_insert'))
    nbb.reindex(os.path.join(BUILD_DIR, 'nb_grammar_insert'), insert=True)

    # Tests with nb_grammar_tighten

    NB_GRAMMAR_TIGHTEN = [
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

    logging.info("\n# Creating notebooks in %s",
                 os.path.join(os.path.dirname(__file__),
                              BUILD_DIR, 'nb_grammar_tighten'))
    bt.create_notebooks(os.path.join(BUILD_DIR, 'nb_grammar_tighten'),
                        NB_GRAMMAR_TIGHTEN)
    logging.info("\n# Reindexing the notebooks in %s",
                 os.path.join(os.path.dirname(__file__),
                              BUILD_DIR, 'nb_grammar_tighten'))
    nbb.reindex(os.path.join(BUILD_DIR, 'nb_grammar_tighten'), tighten=True)

    # Test with complement

    NB_COMPLEMENT = [
        '00.00-Introduction.ipynb',
        '01.00.Lecture-Math_Background.ipynb',
        '01.01-Vector_Calculus.ipynb',
        '01.02-Rigid_Motions.ipynb',
        '02.00.Lecture-Kinematics.ipynb',
        '02.01.Lecture-Velocity_and_Acceleration.ipynb',
        '02.02.Lecture-Different_Types_of_Motions_and_Their_Components.ipynb',
        '03.00.Lecture-Dynamics.ipynb',
        '03.01..Part-Force_and_Momentum.ipynb',
        '03.02..Part-Orbits_of_Planets_and_Satellites.ipynb',
        '03.03..Part-Interception_and_Rendezvous.ipynb',
        '04.00.Lecture-Trajectory_Optimization.ipynb',
        '04.01.Lecture.Part-Performance.ipynb',
        '04.02.Lecture.Part-Gravity_Turn.ipynb',
        '04.03.Lecture.Part-Optimization.ipynb',
        'AA.00-References.ipynb'
    ]

    bt.create_notebooks(os.path.join(BUILD_DIR, 'nb_complement'),
                        NB_COMPLEMENT)

    bt.bind_test(os.path.join(BUILD_DIR, 'nb_complement'),
                 os.path.join(BUILD_DIR, 'nb_complement'),
                 os.path.join(SOURCE_DIR, 'config_nb_complement.yml'))

    # Tests with nb_water

    bt.bind_test(os.path.join(SOURCE_DIR, 'nb_water'),
                 os.path.join(BUILD_DIR, 'nb_water'),
                 os.path.join(SOURCE_DIR, 'config_nb_water.yml'))
