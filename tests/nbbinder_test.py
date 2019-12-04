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

#REG = re.compile(r'(\b\d\d|\b[A][A-Z]|\b[B][A-Z])\.(\d{2}|)(\*|)-(.*)\.ipynb') 

TEST_DIR = 'nbbinder_test_dir'

def create_notebooks(test_dir, nb_filenames):

    if os.path.isdir(test_dir):
        for f in os.listdir(test_dir):
            os.remove(os.path.join(test_dir,f))
    else:
        os.mkdir(test_dir)

    for nb_filename in nb_filenames:
        nb = nbformat.v4.new_notebook()
        nb_reg = nbb.REG_STAR.match(nb_filename)
        nb.cells.insert(0, new_markdown_cell('# ' + nb_reg.group(5).replace('_', ' ')))
        if nb_reg.group(1) == '00':
            text = "That's all for this part of the Front Matter"
        elif nb_reg.group(1)[0] == 'A':
            text = "That's all for this part of the Appendix"
        elif nb_reg.group(1)[0] == 'B':
            text = "That's all for this part of the End Matter"
        else:
            text = "That's all for this Section"
        nb.cells.insert(1, new_markdown_cell(text))
        nbformat.write(nb, os.path.join(test_dir, nb_filename))

if __name__ == '__main__':

    print(f'# Changing to directory {os.path.dirname(__file__)}')
    os.chdir(os.path.dirname(__file__))

    nb_alice = ["00.00-Alice's_Adventures_in_Wonderland.ipynb",
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
                "11.00-Who_Stole_the_Tarts?.ipynb",
                "12.00-Alice's_Evidence.ipynb"
    ]

    print(f"# Creating notebooks in {os.path.join(os.path.dirname(__file__), 'nb_alice')}...")
    create_notebooks('nb_alice', nb_alice)
    print('... notebooks created')
    print(f"\n# Reestructuring the notebooks in {os.path.join(os.path.dirname(__file__), 'nb_alice')}")
    nbb.restructure('nb_alice')

    print("\n# Binding notebooks with config file 'nb_alice_config.yml'")
    nbb.bind_from_configfile('nb_alice_config.yml')

#    quit()

    nb_filenames_2 = ['00.00-Front_Page.ipynb',
                      '00.00i-Foreword.ipynb', 
                      '00.00ii-Dedicatory.ipynb',
                      '00.01-Introduction.ipynb', 
                      '01.00-The_Beginnings.ipynb',
                      '01.01-Joyful_Years.ipynb',
                      '01.02-First_Steps.ipynb',
                      '01.02i-A_Scary_Moment.ipynb',
                      '01.02j-Back_to_Normal.ipynb',
                      '01.03-Speaking_Out.ipynb',
                      '01i.00-Growing_Up.ipynb',
                      '01i.01-Out_in_the_Wild.ipynb',
                      '01i.02-Calming_Down.ipynb',
                      '01ii.00-Maturing.ipynb',
                      '01ii.01-Building_a_Nest.ipynb',
                      '01ii.02-History_Repeats_Itself.ipynb',
                      '02.00-Growing_Old.ipynb',
                      '02a.00-Melancholia.ipynb',
                      '02b.00-Revival.ipynb',
                      '02c.00-The_End.ipynb',
                      'AA.00-Appendix_A.ipynb',
                      'AAi.00-Appendix_B.ipynb',
                      'AB.00-Appendix_C.ipynb',
                      'BA.00-Bibliography.ipynb',
                      'BAi.00-Index.ipynb']

    print(f"\n# Creating notebooks in {os.path.join(os.path.dirname(__file__), 'test_dir_2')}")
    create_notebooks('test_dir_2', nb_filenames_2)
    print(f"\n# Reestructuring the notebooks in {os.path.join(os.path.dirname(__file__), 'test_dir_2')}")
    nbb.restructure('test_dir_2')

    nb_filenames_3 = ['00.00-Front_Page.ipynb',
                      '00.01-Introduction.ipynb', 
                      '01.00-The_Beginnings.ipynb',
                      '01.01-Joyful_Years.ipynb',
                      '01.02-First_Steps.ipynb',
                      '01.02i-A_Scary_Moment.ipynb',
                      '01.02i-A_Scary_Moment_Alternative.ipynb',
                      '01.02j-Back_to_Normal.ipynb',
                      '01.03-Speaking_Out.ipynb',
                      '01i.00-Growing_Up.ipynb',
                      '01i.01-Out_in_the_Wild.ipynb',
                      '01i.01-Out_in_the_Wild_Alternative.ipynb',
                      '01i.02-Calming_Down.ipynb',
                      '02.00-Growing_Old.ipynb',
                      '02a.00-The_End.ipynb',
                      'AA.00-Appendix.ipynb',
                      'AAi.00-Appendix.ipynb',
                      'AB.00-Appendix.ipynb',
                      'BA.00-Bibliography.ipynb',
                      'BAi.00-Index.ipynb']

    print(f"\n# Creating notebooks in {os.path.join(os.path.dirname(__file__), 'test_dir_3')}")
    create_notebooks('test_dir_3', nb_filenames_3)
    print(f"\n# Reestructuring the notebooks in {os.path.join(os.path.dirname(__file__), 'test_dir_3')}")    
    nbb.restructure('test_dir_3')

    print(f"\n# Creating notebooks in {os.path.join(os.path.dirname(__file__), 'test_dir_2_bound')}")
    create_notebooks('test_dir_2_bound', nb_filenames_2)
    print(f"\n# Binding the notebooks in {os.path.join(os.path.dirname(__file__), 'test_dir_2_bound')}")
    nbb.bind_from_configfile('config_test_dir_2_bound.yml')

    print("\n# Binding notebooks with config file 'config1.yml'")
    nbb.bind_from_configfile('config1.yml')

    print("\n# Binding notebooks with config file 'config2.yml'")
    nbb.bind_from_configfile('config2.yml')

    print("\n# Binding notebooks with config file 'config3.yml'")
    nbb.bind_from_configfile('config3.yml')

    print("\n# Binding notebooks with config file 'config4.yml'")
    nbb.bind_from_configfile('config4.yml')

    print("\n# Binding notebooks with config file 'config5.yml'")
    nbb.bind_from_configfile('config5.yml')

    print("\n# Binding notebooks with 'nbb.bind()'")
    nbb.bind(toc_nb_name = '00.00-Front_Page.ipynb',
            header = 'Test 3 for the nbbinder module',
            core_navigators=['00.00-Front_Page.ipynb', 
            'BA.00-References.ipynb'],                  
            app_to_notes_path='notebooks',
            show_full_entry_in_nav=True)