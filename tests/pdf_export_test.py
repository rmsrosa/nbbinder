#!/anaconda3/envs/nbbinder/bin/python
# -*- coding: utf-8 -*-
'''
PDF Export NBBinder test
'''

import os
import logging

import basetest as bt

# Logging level
logging.basicConfig(level=logging.WARNING)

#bt.logger.setLevel(logging.INFO)
#nbb.logger.setLevel(logging.INFO)

# Directories
BUILD_DIR = 'nb_export_builds'
SOURCE_DIR = 'nb_source'

if __name__ == '__main__':

    bt.change_to_file_dir()

    bt.create_build_dir(BUILD_DIR)

    bt.bind_test(os.path.join(SOURCE_DIR, 'nb_water'),
                 os.path.join(BUILD_DIR, 'nb_water_export'),
                 os.path.join(SOURCE_DIR, 'config_nb_water_export.yml'))
