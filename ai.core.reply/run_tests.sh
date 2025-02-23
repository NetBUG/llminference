#!/bin/bash
cd ai.core.reply

docker build . -t llm_inferrer

# TODO replace ENTRYPOINT in Dockerfile with python3 -m pytest
docker run llm_inferrer pytest
