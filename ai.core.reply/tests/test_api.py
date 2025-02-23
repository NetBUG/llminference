#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/02/20 13:00
# @Author  : Oleg Urzhumtsev aka @netbug
# @Site    : https://github.com/NetBUG/llminference
# @File    : tests/test_api.py
# This file contains test for instance/app.py

import pytest
import sys

from fastapi.testclient import TestClient

from instance.logger import logger as base_logger
logger = base_logger.bind(corr_id='TEST_API')
# from instance.parameters import InferenceParameters, MinimalInferenceParameters

# InferenceParameters.model_name = MinimalInferenceParameters.model_name

class MockLLMPipeline:
    def __init__(self, device: str):
        logger.info(f'Loading no model for tests')

    def generate(self, text: str):
        return 'Hello, World!'

@pytest.fixture()
def mock_lib_installed():
    module = type(sys)("core")
    module.submodule = type(sys)("gen_pipeline")
    module.submodule.LLMPipeline = MockLLMPipeline
    sys.modules["core"] = module
    sys.modules["core.gen_pipeline"] = module.submodule

    yield

    del sys.modules["core"]
    del sys.modules["core.gen_pipeline"]


def test_mock_lib_installed(mock_lib_installed):
    # Import the main function from the app module
    from instance.app import app
    assert "core.gen_pipeline" in sys.modules


def test_api_running(mock_lib_installed):
    # Import the main function from the app module
    from instance.app import app as app_main
    client = TestClient(app_main)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == { "message": "Hello, World!" }
