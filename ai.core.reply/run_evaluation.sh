#!/bin/bash
cd ai.core.reply
docker build . -t llm_inferrer

docker rm -f ai_core_eval
docker run --ipc host --gpus 0 -e LOGURU_LEVEL=INFO --name ai_core_eval llm_inferrer python3 evaluation/evaluate.py -m trl
docker commit ai_core_eval ai_core_eval_1
docker run --ipc host --gpus 0 -e LOGURU_LEVEL=INFO --name ai_core_eval_1 ai_core_eval_1 python3 evaluation/evaluate.py -m vllm
