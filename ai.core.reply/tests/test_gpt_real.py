import pytest
import sys

# As from https://fastapi.tiangolo.com/tutorial/testing/#testing-file
from fastapi.testclient import TestClient

from core.gen_pipeline import LLMPipeline
from instance.logger import logger as base_logger
from instance.parameters import InferenceParameters, MinimalInferenceParameters

logger = base_logger.bind(corr_id='TEST_GPT')
InferenceParameters.model_name = MinimalInferenceParameters.model_name
InferenceParameters.model_params["num_return_sequences"] = 1
InferenceParameters.model_params["do_sample"] = True

def test_e2e_real_cpu():
    # Import the main function from the app module
    pipeline = LLMPipeline()    # params with gpt2 and cpu
    response = pipeline.generate("Hello, World!")
    assert type(response) == tuple
    assert len(response) == 2
    assert type(response[0]) == str
    assert type(response[1]) == bool
