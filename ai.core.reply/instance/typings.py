#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/17 15:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : instance/typings.py
# This file contains common data types


class FilteringAction:
    REJECT = 'reject'       # Return status telling the generation was declined
    FILTER = 'filter'       # Filter out blacklisted words
    STUB = 'stub'           # Use one of predefined stubs instead of generation
    NONE = 'none'           # Do nothing

class EmptyResponseException(Exception):
    def __init__(self, name: str):
        self.name = name


class RequestContext:
    logger = None
    query = ""
    history = []
    response = None
    filtered = False
    status = 'ok'
