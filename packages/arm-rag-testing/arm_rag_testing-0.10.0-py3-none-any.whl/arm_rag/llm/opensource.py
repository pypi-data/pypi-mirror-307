import torch
from arm_rag.config import CONFIG
from transformers import AutoTokenizer, AutoModelForCausalLM



class Open_Source:
    def __init__(self, token, model=None, max_tokens=None):
        # self.token = os.getenv('HUGGINGFACE_TOKEN')
        self.token = token
        if model:
            self.tokenizer = AutoTokenizer.from_pretrained(model)
            self.model = AutoModelForCausalLM.from_pretrained(
                model,
                device_map="auto" if torch.cuda.is_available() else None,
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32
            ) 
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(CONFIG['open_source']['model'])
            self.model = AutoModelForCausalLM.from_pretrained(
                CONFIG['open_source']['model'],
                device_map="auto" if torch.cuda.is_available() else None,
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32
            )  
        if max_tokens:
            self.max_tokens = max_tokens
        else:  
            self.max_tokens = CONFIG['open_source']['max_tokens']
        self.user_prompt = CONFIG['open_source']['prompt_template'][1]['user']
        self.system_prompt = CONFIG['open_source']['prompt_template'][0]['system']
        self.temperature = CONFIG['open_source']['temperature']
    

    def tokenize(self, input_text):
        input_ids = self.tokenizer(input_text, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
        return input_ids
    

    def decode(self, input_ids):
        return self.tokenizer.decode(input_ids[0], skip_special_tokens=True)
    

    def generate_response(self, input_text: str, context: str) -> str:
        # Format user prompt
        combined_prompt = self.user_prompt.format(
            context=context,
            question=input_text
        )
        combined_prompt_ids = self.tokenize(combined_prompt) 
        output_ids = self.model.generate(**combined_prompt_ids, max_new_tokens=32)
        output = self.decode(output_ids)
        
        return output
    