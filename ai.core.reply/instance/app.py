#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/17 15:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : instance/app.py
# This file contains main application entrypoint

import argparse
from instance.logger import logger as base_logger
from instance.typings import EmptyResponseException, RequestContext
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import random
import uvicorn

from core.gen_pipeline import LLMPipeline

logger = base_logger.bind(corr_id='APP')

ap = argparse.ArgumentParser()
ap.add_argument('-p', '--port', help='Port to be listened', type=int, default=8000)
ap.add_argument('-i', '--ip', help='IP of the interface to listen. Defaults to 0.0.0.0', default='0.0.0.0')
ap.add_argument('-m', '--model', help='trl or vllm model', default='vllm')
ap.add_argument('-d', '--device', help='Device for model deployment', default=None)

args = ap.parse_args()

app = FastAPI()

# Load model
model_wrapper = LLMPipeline(args.device, model_type=args.model)

"""
@api {get} / Service status
@apiDescription A default endpoint to check the status of the service
@apiName Main
@apiGroup Main

@apiSuccess {String} message Status of the system
"""
@app.get('/')
def index():
    return JSONResponse({ 'status': "ok" if model_wrapper.is_ready() else "loading" })

"""
@api {post} /generate Perform query
@apiDescription Perform a query to the model. Should be sent as a JSON object
@apiName Query
@apiGroup LLM

@apiParam {String} text User's query

@apiSuccess {String} response Response generated by the model
@apiSuccess {String} query Repetition of the user's query
@apiSuccess {String} filtered True if the message was filtered
@apiSuccess {String} status Status of the query, should be 'ok' or 'error'

@apiError ValueError The query provided is not valid while filtering is set to REJECT
@apiError Exception The query resulted in an unknown error
"""
@app.post('/generate')
async def generate(payload: dict):
    context = RequestContext()
    # Initialize logger with uniqie correlation ID
    context.request_id = random.randint(1000, 9999)
    context.logger = base_logger.bind(corr_id='REQ_%d' % context.request_id)
    try:
        context.query = payload['text']
        await model_wrapper.generate(context)
        return { "query": context.query,
                 "message": context.response,
                 "filtered": context.filtered,
                 "status": context.status }
    except Exception as e:
        logger.error(f"Error obtaining text: {e}")
        raise HTTPException(status_code=400, detail={ "message": str(e) })

def main():
    uvicorn.run(app, host=args.ip, port=args.port)

if __name__ == '__main__':
    main()
