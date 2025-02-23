#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/23 17:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : instance/model_gen.py
# This file contains vLLM-based GPT generation model
# It is used to generate responses for the chatbot

import time
import torch
from typing import List, Tuple
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

from core.utils.texttools import filter_non_printable_symbols
from instance.logger import logger as base_logger
from instance.parameters import InferenceParameters, VLLMParams

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
        self.model = LLM(
                            model=VLLMParams.model_name,
                            dtype=torch.bfloat16,
                            gpu_memory_utilization=VLLMParams.MAX_GPU_MEM,
                            max_model_len=VLLMParams.MAX_MODEL_SEQ_LEN,
                            task='generate',
                            device=self.device,
                            enable_prefix_caching=True,
                        )


    def generate_text(self, query: str) -> Tuple[str, List[float]]:
        """
        Generates a response to the context
        """
        context_str = InferenceParameters.system_prompt.format(user_query=query)

        generated_texts = []
    
        with torch.inference_mode():
            start = time.time()
            outputs = self.model.generate(
                                [context_str],
                                [self.sampling_params],
                                use_tqdm=False
                                )
            self.logger.debug(f"Generation: {time.time() - start:.3f} seconds; T = {self.sampling_params.temperature:.2f}")

        generated_texts = [filter_non_printable_symbols(o.text) for o in outputs[0].outputs]
        generated_texts = [generated_text for generated_text in generated_texts if generated_text.strip() != ""]

        return generated_texts
