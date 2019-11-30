#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Notebook Binder test for the collection of notebooks in this directory
'''

from context import nbbinder as nbb

if __name__ == '__main__':

# Add contents, book info, and navigation bars
    nbb.bind(toc_nb_name = '00.00-Front_Page.ipynb',
             header = 'Test 3 for the nbbinder module',
             core_navigators=['00.00-Front_Page.ipynb', 
               'BA.00-References.ipynb'],                  
             app_to_notes_path='notebooks',
             show_full_entry_in_nav=True)
