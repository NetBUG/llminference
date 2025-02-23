#!/bin/bash
cd ai.core.reply
docker rm -f ai_core_tests

docker build . -t llm_inferrer

# TODO replace ENTRYPOINT in Dockerfile with python3 -m pytest
docker run --name ai_core_tests llm_inferrer python3 -m pytest
