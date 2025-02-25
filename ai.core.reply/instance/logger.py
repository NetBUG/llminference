#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/25 22:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : instance/logger.py
# This file contains a wrapper around loguru logger

from loguru import logger
import sys

# Show which module makes output
corr_id = 'BASIC'

logger.remove()
logger.add(sys.stdout, format="[{level.icon}  {level.name[0]}]\t{time:YYYY-MM-DD HH:mm:ss.SSS}\tCID: {extra[corr_id]}\t{message}")

if __name__ == "__main__":
    # Pytest does not help with checkout output highlighting
    logger = logger.bind(corr_id=corr_id)
    logger.warning("This is a module and should not be run directly. Running self-tests...")
    logger.info("Okay!")
