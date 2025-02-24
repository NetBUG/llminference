#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/23 23:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : tests/test_gpt_real.py
# This file contains test for core/gen_pipeline.py

from core.gen_pipeline import LLMPipeline
from instance.logger import logger as base_logger
from instance.parameters import InferenceParameters, MinimalInferenceParameters
from instance.typings import RequestContext

logger = base_logger.bind(corr_id='TEST_GPT')
InferenceParameters.model_name = MinimalInferenceParameters.model_name
InferenceParameters.model_params["num_return_sequences"] = 1
InferenceParameters.model_params["do_sample"] = True

def test_e2e_real_cpu():
    # Import the main function from the app module
    pipeline = LLMPipeline()    # params with gpt2 and cpu
    context = RequestContext()
    context.query = "How are you doing?"
    context.logger = logger
    pipeline.generate(context)
    assert type(context) == RequestContext
    assert type(context.raw_responses) == list
    assert len(context.raw_responses) == InferenceParameters.model_params["num_return_sequences"]
    assert type(context.response) == str
    assert type(context.filtered) == bool
