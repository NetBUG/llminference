# File with parameters used for inference

class FilteringAction:
    REJECT = 'reject'       # Return status telling the generation was declined
    FILTER = 'filter'       # Filter out blacklisted words
    STUB = 'stub'           # Use one of predefined stubs instead of generation
    NONE = 'none'           # Do nothing

class EmptyResponseException(Exception):
    def __init__(self, name: str):
        self.name = name

MAX_NEW_TOKENS = 50         # 

# Version for 24+ Gb GPU RAM (fits into 16 Gb with small context)
class InferenceParameters:
    model_name = 'allenai/Llama-3.1-Tulu-3.1-8B' 
    system_prompt = "You are Tulu 3, a helpful and harmless AI Assistant built by the Allen Institute for AI.<|user|>\n{user_query}\n<|assistant|>\n"
    model_params = {
        "max_new_tokens": MAX_NEW_TOKENS, # max_tokens
        # "num_beams": 2,
        "num_return_sequences": 2,
        "temperature": 0.55,
        "early_stopping": False,
        "no_repeat_ngram_size": 3,
        # "repetition_penalty": 1.15,
        # "do_sample": True
    }

# Version for 4+ Gb GPU RAM
class MinimalInferenceParameters:
    model_name = 'microsoft/DialoGPT-small' 
    system_prompt = "You are a bot called. Answer a question for a user please.\nUser:{user_query}\nBot:"
    prompt = "<|user|>\nHow are you doing?\n<|assistant|>\n<|endoftext|>"
    model_params = {
        "max_new_tokens": MAX_NEW_TOKENS, # max_tokens
        "num_beams": 2,
        "num_return_sequences": 2,
        "temperature": 0.8,
        "early_stopping": True,
        "no_repeat_ngram_size": 3,
        # "repetition_penalty": 1.15,
        "eos_token_id": 50256,
        "pad_token_id": 50256,
        "do_sample": True
    }

class VLLMParams:
    use_sampling_params = True
    context_reduce_factor = 1.

    generation_params_sample = {
        "n": 3,
        "best_of": 3,
        "temperature": 0.8,
        "top_p": 0.8,
        "use_beam_search" : False,
        "repetition_penalty": 1.15,
        "presence_penalty": 0.1,
        "frequency_penalty": 0.2,
        "length_penalty": 1.0,
        "early_stopping": False,
        "max_tokens": MAX_NEW_TOKENS,
        "stop_token_ids": [EOM_ID],
        "ignore_eos": False,
        "skip_special_tokens": True,
        "spaces_between_special_tokens": True
    }

class FilteringParameters:
    # Blacklisting in preprocessor
    blacklist_file = "data/prefilter_blacklist.json"
    blacklist = None
    preprocessor_action = FilteringAction.REJECT

    # Limit incoming messages in characters
    length_limit_soft = 140
    length_limit_hard = 200

    # Filtering model in postprocessor
    stub_templates_file = "data/postfilter_stubs.json"
    # filtering_model_name = 'facebook/bart-large-cnn'
    model_name = 's-nlp/roberta_toxicity_classifier'
    postprocessor_filtering_threshold = 3.5
    postprocessor_action = FilteringAction.STUB


# Version for 8 Gb GPU RAM

# Version for CPU

# Version for Apple M1+ CPU
