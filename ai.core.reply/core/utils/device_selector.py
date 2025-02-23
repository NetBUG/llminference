#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/23 14:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : core/utils/device_selector.py
# Simple device selector for PyTorch

import torch

from instance.logger import logger as base_logger

logger = base_logger.bind(corr_id='DEVSEL')

def select_device(device: str | None = None) -> torch.device:
    if device is None:
        if torch.backends.mps.is_available():
            device = torch.device("mps")
        elif torch.cuda.is_available():
            return torch.device("cuda")
    else:
        try:
            return torch.device(device)
        except Exception as e:
            logger.warning(f"Error selecting device: {e}")
    
    return torch.device("cpu")
