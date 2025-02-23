#!/bin/bash
cd ai.core.reply

docker build . -t llm_inferrer

docker run llm_inferrer pytest
