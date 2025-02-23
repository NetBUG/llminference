#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/23 14:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : tests/test_preprocessor.py
# This file contains test for core/preprocessor.py

import pytest
import sys

from core.preprocessor import Preprocessor
from instance.parameters import FilteringParameters

preprocessor = Preprocessor()

def test_trim_message():
    """
        Test that preprocessor.trim_message() works as expected
    """
    message = "Hello, World!"
    assert preprocessor.trim_message(message) == (message, False)

    message = "Hello, World! I am writing a long message to test the trim function while it exceeds the limit of 200 characters. This is a long test message. This is stripped by sentence boundary as it is the second part needing to fit into 200 characters."
    trimmed = "Hello, World! I am writing a long message to test the trim function while it exceeds the limit of 200 characters. This is a long test message."
    assert preprocessor.trim_message(message) == (trimmed, True)

    message = "Hello, World, I am writing a long message to test the trim function while it exceeds the limit of 200 characters This is a long test message This is stripped by word boundary as it is the second part needing to fit into 200 characters"
    trimmed = "Hello, World, I am writing a long message to test the trim function while it exceeds the limit of 200 characters This is a long test message This is stripped by word boundary as it is the second part"
    assert preprocessor.trim_message(message) == (trimmed, True)

    message = "HelloWorld_Iamwriting_a_long_message_with_abracadabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabra135brabrabra_someothercraphere_brabrabrabrabrabrabrabrabrabra196brabrabrabra"
    trimmed = "HelloWorld_Iamwriting_a_long_message_with_abracadabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabrabra135brabrabra_someothercraphere_brabrabrabrabrabrabrabrabrabra196brabr"
    assert preprocessor.trim_message(message) == (trimmed, True)

def test_check_blacklist():
    """
        Test that preprocessor.check_blacklist() works as expected
    """
    assert preprocessor.check_blacklist("Hello, World!") == False
    assert preprocessor.check_blacklist("Hello, functional world!") == True
    assert preprocessor.check_blacklist("Hello, FUNCTIONAL WORLD!") == True

def test_filter_text():
    """
        Test that preprocessor.filter_text() works as expected
    """
    message = "Hello, World!"
    assert preprocessor.filter_text(message) == ("Hello, World!", False)

    message = "Hello, World! I am writing a long message to test the trim function while it exceeds the limit of 200 characters. This is a long test message. This is stripped by sentence boundary as it is the second part needing to fit into 200 characters."
    trimmed = "Hello, World! I am writing a long message to test the trim function while it exceeds the limit of 200 characters. This is a long test message."
    assert preprocessor.filter_text(message) == (trimmed, False)

    # This should be rejected with default configuration
    message = "Hello, World! I am writing a FUNCTIONAL message to test the trim function while it exceeds the limit of 200 characters. This is a long test message. This is stripped by sentence boundary as it is the second part needing to fit into 200 characters."
    trimmed = "Hello, World! I am writing a FUNCTIONAL message to test the trim function while it exceeds the limit of 200 characters. This is a long test message."
    assert preprocessor.filter_text(message) == (trimmed, True)
