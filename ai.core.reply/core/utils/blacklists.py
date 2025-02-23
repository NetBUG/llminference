#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/20 19:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : core/utils/blacklists.py
# This file contains the logic to load lists from a JSON file
# It can be upgraded to include more complex logic, e.g. with 
# SQL database, periodically updating lists, etc.

import json
from instance.logger import logger as base_logger

logger = base_logger.bind(corr_id='BLACKLIST')

def load_lists(blacklists_file):
    """
    Load blacklists from a JSON file
    @param blacklists_file: path to the file
    @return Object containing blacklists
    """
    localObject = []
    if blacklists_file.endswith('.json'):
        try:
            with open(blacklists_file, 'r') as stream:
                localObject = json.load(stream)
        except Exception as e:
            logger.error(f"Error loading the file {blacklists_file}, continuing without preprocessing")
            logger.exception(e)
    else:
        logger.error(f"The file {blacklists_file} cannot be loaded as it does not seem JSON file!")
    return localObject
