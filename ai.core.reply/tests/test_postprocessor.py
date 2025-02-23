#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/23 14:30
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : tests/test_postprocessor.py
# This file contains test for core/postprocessor.py


import torch

from core.postprocessor import Postprocessor
from core.utils.device_selector import select_device
from instance.parameters import FilteringParameters

postprocessor = Postprocessor(select_device())

def test_get_toxic_score():
    """
        Test that postprocessor.get_toxic_score() works as expected by filtering some phrases
    """

    msg = "Hello, World!"
    assert postprocessor.get_toxic_score(msg) < FilteringParameters.postprocessor_filtering_threshold

    msg = "Hello, World! Go fuck yourself"
    assert postprocessor.get_toxic_score(msg) < FilteringParameters.postprocessor_filtering_threshold


def test_postprocessing():
    """
        Test that postprocessor.output_post_processing() strips replies properly
    """
    msg = "Hello, World!"
    assert postprocessor.output_post_processing(msg) == msg

    msg = "Hello, World!\n\n"
    assert postprocessor.output_post_processing(msg) == msg.strip()

    msg = "\n\nHello, World!"
    assert postprocessor.output_post_processing(msg) == msg.strip()


def test_assess_response():
    """
        Test that postprocessor.assess_response behaves as expected
    """

    history = ["Hello, World!"]
    responses = ["Hello, World!", "Hello, World! Go fuck yourself"]
    assert postprocessor.assess_response(history, responses[0]) == True
    assert postprocessor.assess_response(history, responses[1]) == False


def test_filter_context():
    """
        Test that postprocessor.filter_context() removes a bad reply
    """

    history = ["Hello, World!"]
    responses = ["Hello, World!", "Hello, World! Go fuck yourself"]
    assert postprocessor.filter_context(history, responses) == (responses[0], False)
