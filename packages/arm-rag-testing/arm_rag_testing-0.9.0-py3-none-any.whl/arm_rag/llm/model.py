from .gpt import Gpt
from .claude import Claude
from .opensource import Open_Source


def get_model(model_type, api_key, model, max_tokens):
    if model_type == 'gpt':
        return Gpt(api_key, model, max_tokens)
    elif model_type == 'claude':
        return Claude(api_key, model, max_tokens)
    elif model_type == 'open_source':
        return Open_Source(api_key, model, max_tokens)
    else:
        raise ValueError("Invalid model_type")