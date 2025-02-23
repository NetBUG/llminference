#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/18 11:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : core/gen_pipeline.py
# This file contains the main pipeline for the model

import random
import torch
from typing import Tuple

from core.core_transformers import ModelGenerator
from instance.logger import logger as base_logger
from instance.parameters import FilteringAction, FilteringParameters, InferenceParameters
from core.preprocessor import Preprocessor
from core.postprocessor import Postprocessor
from core.utils.device_selector import select_device

class LLMPipeline:
    def __init__(self, device: str | None = None):
        self.device = select_device(device)

        self.logger = base_logger.bind(corr_id='PIPELINE')

        self.logger.info(f'Loading model: {InferenceParameters.model_name} to device: {self.device}')
        self.model = ModelGenerator(self.device)
        self.preprocessor = Preprocessor()
        self.postprocessor = Postprocessor(self.device)

    def is_ready(self) -> bool:
        return self.model and self.postprocessor.is_ready()

    def generate(self, text: str) -> Tuple[str, bool]:
        try:
            text, pre_filtered = self.preprocessor.filter_text(text)
            if FilteringParameters.preprocessor_action == FilteringAction.STUB and pre_filtered:
                return random.choice(self.preprocessor.stubs), True
            raw_responses = self.model.generate_text(text)
            response, post_filtered = self.postprocessor.filter_context([text], raw_responses)
            if FilteringParameters.postprocessor_action == FilteringAction.STUB and post_filtered:
                return random.choice(self.postprocessor.stubs), True
            return response, False
        except ValueError as e:
            self.logger.error(f"Filtering text raised exception: {e}")
            raise e
