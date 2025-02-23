#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/17 15:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : instance/core_transformers.py
# This file contains main application entrypoint

import os
import torch
import time
from transformers import AutoModelForCausalLM, AutoTokenizer

from instance.logger import logger as base_logger
from instance.parameters import InferenceParameters

class ModelGenerator:
    def __init__(self, device: str = 'cpu'):
        self.token = os.environ.get('HF_TOKEN', None)
        self.model_name = InferenceParameters.model_name
        self.logger = base_logger.bind(corr_id='MODELGEN')
        self.device = torch.device(device)

        # Load model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=self.token)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name,
                                                          token=self.token,
                                                          torch_dtype=torch.float16,
                                                          # use_flash_attention_2=True,
                                                          low_cpu_mem_usage=True,
                                            ).to(self.device)

    def generate_text(self, text: str):
        prompt = InferenceParameters.system_prompt.format(user_query=text)

        self.logger.debug(f"Generating response for: {prompt}")
        encoded_context = self.tokenizer.encode(prompt,
                                                return_tensors='pt',
                                                return_attention_mask=True,
                                                padding=True).to(self.device)
        encoded_context_len = len(encoded_context[0])

        responses_ids = None
        with torch.inference_mode():
            start = time.time()
            responses_ids = self.model.generate(
                encoded_context, # encoded_context["input_ids"],
                # attention_mask=encoded_context["attention_mask"],
                pad_token_id=self.tokenizer.eos_token_id,
                **InferenceParameters.model_params
                # Also bad_words_ids may be used to prohibit model from using some tokens
            )
            self.logger.debug("Generation: %.3f seconds" % (time.time() - start))

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        responses = [self.tokenizer.decode(logits[encoded_context_len:], \
                                           skip_special_tokens=True) for logits in responses_ids]

        self.logger.debug(f"Raw responses: {responses}")

        return responses
