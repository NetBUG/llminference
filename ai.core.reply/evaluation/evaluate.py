#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/23 18:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : evaluation/evaluate.py
# This file contains evaluation script for a set model

import argparse
import asyncio
import json
import random
import time
import torch

from core import gen_pipeline
from core.utils.device_selector import select_device
from instance.logger import logger as base_logger
from instance.parameters import EmptyResponseException
from instance.typings import RequestContext

logger = base_logger.bind(corr_id='EVAL')

ap = argparse.ArgumentParser()
ap.add_argument('-m', '--mode', help='Mode: `trl` or `vllm`', default='trl')
ap.add_argument('-i', '--iterations', help='Iterations (defaults to 100)', type=int, default=100)
args = ap.parse_args()

def get_tokenizer(model: gen_pipeline.LLMPipeline) -> callable:
    """Get tokenizer from the model"""
    return model.model.tokenizer

async def evaluate(model: object, questions: list[str], iterations: int = 100) -> dict:
    """Evaluate a set of questions and answers"""

    context = RequestContext()
    context.query = questions[0]
    context.logger = logger

    await model.generate(context) # Warm-up the model

    for i in range(iterations):
        start = time.time()
        try:
            context.query = random.choice(questions)
            model.generate(context)
        except EmptyResponseException as e:
            pass
        except Exception as e:
            logger.error(f"error! {e}")
        q_len = len(get_tokenizer(model)(context.query).input_ids)
        a_len = len(get_tokenizer(model)(context.response).input_ids)
        logger.debug(f"Q: {context.query} [{q_len}]\tA: {context.response} [{a_len}], T={time.time() - start:.3f}")

    # Need 

    results = {}

    return results

if __name__ == '__main__':
    device = select_device() # Select the best device for the model
    model = gen_pipeline.LLMPipeline(device, model_type=args.mode)

    with open('data/eval_queries.json', 'r') as f:
        data = json.load(f)
        logger.info(f"Evaluating on {device} -- {torch.cuda.get_device_name()} - {args.mode.upper()} mode")

        n_iterations = args.iterations

        start = time.time()
        asyncio.run(evaluate(model, data['short_questions'], n_iterations))
        logger.info(f'Short questions evaluated: {time.time() - start:.3f}s, average {n_iterations * 60 / (time.time() - start):.3f} RPM')

        start = time.time()
        asyncio.run(evaluate(model, data['long_questions'], n_iterations))
        logger.info(f'Long questions evaluated: {time.time() - start:.3f}s, average {n_iterations * 60 / (time.time() - start):.3f} RPM')

        start = time.time()
        asyncio.run(evaluate(model, data['long_questions'] + data['short_questions'], n_iterations))
        logger.info(f'Mixed dataset evaluated: {time.time() - start:.3f}s, average {n_iterations * 60 / (time.time() - start):.3f} RPM')
