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
from instance.typings import RequestContext

class ModelGenerator:
    def __init__(self, device: str = 'cpu'):
        self.token = os.environ.get('HF_TOKEN', None)
        self.model_name = InferenceParameters.model_name
        self.logger = base_logger.bind(corr_id='GEN_MDL')
        self.device = torch.device(device)

        # Load model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=self.token)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name,
                                                          token=self.token,
                                                          torch_dtype=torch.float16,
                                                          low_cpu_mem_usage=True,
                                            ).to(self.device)

        # [[self.tokenizer.eos_token_id]]
        self.bad_words_ids = self.tokenizer(InferenceParameters.bad_words).input_ids
        self.tokenizer.pad_token = self.tokenizer.eos_token       

    async def generate_text(self, text: str, context: RequestContext):
        prompt = InferenceParameters.system_prompt.format(user_query=text)

        context.logger.debug(f"Generating response for: {prompt}")
        start = time.time()
        encoded_context = self.tokenizer(prompt,
                                                return_tensors='pt',
                                                padding=True).to(self.device)
        context.logger.debug("Tokenization: %.3f seconds" % (time.time() - start))
        encoded_context_len = len(encoded_context[0])

        responses_ids = None
        with torch.inference_mode():
            responses_ids = self.model.generate(
                input_ids=encoded_context["input_ids"],
                pad_token_id=self.tokenizer.eos_token_id,
                attention_mask=encoded_context["attention_mask"],
                **InferenceParameters.model_params,
                bad_words_ids=self.bad_words_ids,
            )

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        responses = [self.tokenizer.decode(logits[encoded_context_len:], \
                                           skip_special_tokens=True) for logits in responses_ids]

        context.logger.trace(f"Raw responses: {responses}")

        return responses
