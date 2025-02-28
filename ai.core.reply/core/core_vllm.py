#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/23 17:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : instance/model_gen.py
# This file contains vLLM-based GPT generation model
# It is used to generate responses for the chatbot

import asyncio
import json
import time
import torch
from typing import AsyncGenerator, List, Tuple
from transformers import AutoTokenizer
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.sampling_params import SamplingParams

from core.utils.texttools import filter_non_printable_symbols
from instance.logger import logger as base_logger
from instance.parameters import InferenceParameters, VLLMParams
from instance.typings import RequestContext, EmptyResponseException

# FIXME See https://docs.vllm.ai/en/latest/getting_started/examples/basic_with_model_default_sampling.html

gpt_logger = base_logger.bind(corr_id='GEN_VLLM')

class ModelGenerator():
    " Class containing GPT model "
    error_count = 0
    logger = gpt_logger

    def __init__(self, device: str="cuda:0"):
        self.device = device

        self.logger.debug(f"Loading model from {VLLMParams.model_name} to {self.device}")

        self.params = VLLMParams.generation_params_sample
        self.sampling_params = SamplingParams(**self.params)

        # Create an LLM
        self.tokenizer = AutoTokenizer.from_pretrained(VLLMParams.model_name, padding_side='left')
        engine_args = AsyncEngineArgs(model=VLLMParams.model_name,
                            dtype=torch.bfloat16,
                            gpu_memory_utilization=VLLMParams.MAX_GPU_MEM,
                            max_model_len=VLLMParams.MAX_MODEL_SEQ_LEN,
                            task='generate',
                            device=self.device,
                            enable_prefix_caching=True,)
        self.model = AsyncLLMEngine.from_engine_args(engine_args)


    async def generate_text(self, query: str, context: RequestContext) -> Tuple[str, List[float]]:
        """
        Generates a response to the context
        """
        context_str = InferenceParameters.system_prompt.format(user_query=query)

        generated_texts = []
        output = None

        with torch.inference_mode():
            start = time.time()
            results_generator = self.model.generate(
                                context_str,
                                self.sampling_params,
                                request_id=context.request_id,
                                )

            try:
                async for request_output in results_generator:
                    output = request_output
            except asyncio.CancelledError:
                raise EmptyResponseException("Empty response")
            
            self.logger.debug(f"Generation: {time.time() - start:.3f} seconds; T = {self.sampling_params.temperature:.2f}")

        generated_texts = [filter_non_printable_symbols(o.text) for o in output.outputs]
        generated_texts = [generated_text for generated_text in generated_texts if generated_text.strip() != ""]

        return generated_texts
