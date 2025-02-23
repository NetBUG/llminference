#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/18 11:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : core/gen_pipeline.py
# This file contains the main pipeline for the model

import random
import time
from typing import Tuple

from core.core_transformers import ModelGenerator as TRLModelGenerator
from core.core_vllm import ModelGenerator as VLLMModelGenerator
from instance.logger import logger as base_logger
from instance.parameters import FilteringAction, FilteringParameters, InferenceParameters
from core.preprocessor import Preprocessor
from core.postprocessor import Postprocessor
from core.utils.device_selector import select_device

class LLMPipeline:
    def __init__(self, device: str | None = None, model_type: str = 'trl'):
        self.device = select_device(device)

        self.logger = base_logger.bind(corr_id='PIPELINE')

        self.logger.info(f'Loading model: {InferenceParameters.model_name} to device: {self.device}')

        if model_type == 'trl':     # Huggingface TRL
            ModelGenerator = TRLModelGenerator
        elif model_type == 'vllm':  # Very Large Language Model
            ModelGenerator = VLLMModelGenerator
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        self.model = ModelGenerator(self.device)
        self.preprocessor = Preprocessor()
        self.postprocessor = Postprocessor(self.device)

    def is_ready(self) -> bool:
        return self.model and self.postprocessor.is_ready()

    def generate(self, text: str) -> Tuple[str, bool]:
        try:
            preproc_ts = time.time()
            text, pre_filtered = self.preprocessor.filter_text(text)
            self.logger.debug(f"Preprocessing: {time.time() - preproc_ts:.3f} seconds")
            if FilteringParameters.preprocessor_action == FilteringAction.STUB and pre_filtered:
                return random.choice(self.preprocessor.stubs), True

            gen_ts = time.time()
            raw_responses = self.model.generate_text(text)
            self.logger.debug(f"Generation: {time.time() - gen_ts:.3f} seconds")

            postproc_ts = time.time()
            response, post_filtered = self.postprocessor.filter_context([text], raw_responses)
            self.logger.debug(f"Postprocessing: {time.time() - postproc_ts:.3f} seconds")
            if FilteringParameters.postprocessor_action == FilteringAction.STUB and post_filtered:
                return random.choice(self.postprocessor.stubs), True
            return response, False
        except ValueError as e:
            self.logger.error(f"Filtering text raised exception: {e}")
            raise e
