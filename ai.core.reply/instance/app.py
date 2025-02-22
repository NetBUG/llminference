#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/17 15:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : instance/app.py
# This file contains main application entrypoint

import argparse
import os
from instance.logger import logger
from fastapi import FastAPI, HTTPException
import uvicorn

from core.gen_pipeline import LLMPipeline

# Parse command-line arguments
ap = argparse.ArgumentParser()
ap.add_argument('-p', '--port', help='Port to be listened', type=int, default=8000)
ap.add_argument('-i', '--ip', help='IP of the interface to listen. Defaults to 0.0.0.0', default='0.0.0.0')
ap.add_argument('-d', '--device', help='Device for model deployment', default=None)

args = ap.parse_args()

# Set up FastAPI
app = FastAPI()

# Load model
model_wrapper = LLMPipeline(args.device)

@app.get('/')
def index():
    return {'message': 'Hello, World!'}

@app.post('/generate')
def generate(payload: dict):
    try:
        text = payload['text']
        resp, is_filtered = model_wrapper.generate(text)
        return { "query": text, "message": resp, "filtered": is_filtered }
    except ValueError as e:
        logger.error(f"Error obtaining text: {e}")
        raise HTTPException(status_code=400, detail="Sorry, I cannot process this message")

def main():
    uvicorn.run(app, host=args.ip, port=args.port)

if __name__ == '__main__':
    main()
