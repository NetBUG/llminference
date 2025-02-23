#!/bin/bash
cd ai.core.reply

docker build . -t llm_inferrer

docker run --ipc host --gpus 0 -e LOGURU_LEVEL=INFO llm_inferrer python3.10 evaluation/evaluate.py -m trl
docker run --ipc host --gpus 0 -e LOGURU_LEVEL=INFO llm_inferrer python3.10 evaluation/evaluate.py -m vllm
