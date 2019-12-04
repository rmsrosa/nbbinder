#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Notebook Binder test for the collection of notebooks in this directory
'''

import os
from context import nbbinder as nbb

if __name__ == '__main__':

    os.chdir(os.path.dirname(__file__))
# Add contents, book info, and navigation bars
    nbb.bind(toc_nb_name = '00.00-Front_Page.ipynb',
             header = 'Test 3 for the nbbinder module',
             core_navigators=['00.00-Front_Page.ipynb'],                  
             app_to_notes_path='lectures',
             show_full_entry_in_nav=True)
