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

from core.responder import Responder

# Parse command-line arguments
ap = argparse.ArgumentParser()
ap.add_argument('-p', '--port', help='Port to be listened', type=int, default=8000)
ap.add_argument('-i', '--ip', help='IP of the interface to listen. Defaults to 0.0.0.0', default='0.0.0.0')
ap.add_argument('-d', '--device', help='Device for model deployment', default='cpu')

args = ap.parse_args()

# Set up FastAPI
app = FastAPI()

# Load model
model_wrapper = Responder(args.device)

@app.get('/')
def index():
    return {'message': 'Hello, World!'}

@app.post('/generate')
def generate(text: str):
    return model_wrapper.generate(text)

def main():
    uvicorn.run(app, host=args.ip, port=args.port)

if __name__ == '__main__':
    main()
