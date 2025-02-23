#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/19 14:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : core/preprocessor.py
# This file contains the filtering blakclist-based preprocessor

from typing import Tuple

from core.utils.blacklists import load_lists
from instance.logger import logger
from instance.parameters import FilteringAction, FilteringParameters

punct = [".", "!", "?", "\n"]
delim = [" ", "\t"]

class Preprocessor:
    def __init__(self):
        self.filter_blacklist_file = FilteringParameters.blacklist_file
        self.localObject = load_lists(self.filter_blacklist_file)
        self.blacklist = self.localObject["prefilter_blacklist"] if "prefilter_blacklist" in self.localObject else []
        self.stubs = self.localObject["prefilter_blacklist_reasons"] if "prefilter_blacklist_reasons" in self.localObject else []
        self.filtering_action = FilteringParameters.preprocessor_action
        if self.filtering_action == FilteringAction.FILTER and len(self.blacklist) == 0:
            logger.warning(f"Filtering action is set to FILTER, but the field `prefilter_blacklist` is empty in {self.filter_blacklist_file}!")
        if self.filtering_action == FilteringAction.STUB and len(self.stubs) == 0:
            logger.warning(f"Filtering action is set to STUB, but the field `prefilter_blacklist_reasons` is empty in {self.filter_blacklist_file}!")


    def trim_message(self, src_msg: str, soft_limit: int = FilteringParameters.length_limit_soft, \
                    hard_limit: int = FilteringParameters.length_limit_hard) -> Tuple[str, bool]:
        """
        Trims message to a limit. Tries to break by sentence (punctuation) delimiters:
        If not - tries to break by word
        If not - makes a mechanical trim
        @param src_msg: source message
        @param soft_limit: soft limit (try to keep within it preserving sentence and word boundaries)
        @param hard_limit: hard limit (trim to this limit)
        @return: trimmed message; True if message was trimmed
        """
        msg = src_msg[:hard_limit]
        last_delims = [msg.rfind(c) for c in punct]
        # return last before hard after soft
        # return abrupt if len(out_msg) < soft and len(msg) > hard
        if max(last_delims) > soft_limit:
            msg = msg[:max(last_delims) + 1]
        else:
            last_delims = [msg.rfind(c) for c in delim]
            if max(last_delims) > soft_limit:
                msg = msg[:max(last_delims) + 1].strip()
        return msg, len(msg) != len(src_msg)

    def check_blacklist(self, text: str) -> bool:
        return any([word.lower() in text.lower() for word in self.blacklist])

    def filter_text(self, text: str) -> Tuple[str, bool]:
        """
        Filters the text according to the preprocessor action
        @param text: input text
        @return: filtered text; True if message contains blacklisted words
        """
        message, _is_trimmed = self.trim_message(text)
        if self.filtering_action == FilteringAction.FILTER:
            message = " ".join([word for word in text.split() if word.lower() not in self.blacklist])
        return message, self.check_blacklist(message)
    