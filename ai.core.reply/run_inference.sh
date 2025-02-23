#!/bin/bash
cd ai.core.reply

docker build . -t llm_inferrer

# Determine if CUDA devices is available
if [ -z "$CUDA_VISIBLE_DEVICES" ]; then
    echo "CUDA_VISIBLE_DEVICES is not set. Running on CPU."
    docker run -p 8000:80 --name ai_core llm_inferrer:latest
else
    echo "CUDA_VISIBLE_DEVICES is set. Running on GPU."
    docker run --gpus 0 --ipc host -p 8000:80 --name ai_core llm_inferrer:latest
fi
