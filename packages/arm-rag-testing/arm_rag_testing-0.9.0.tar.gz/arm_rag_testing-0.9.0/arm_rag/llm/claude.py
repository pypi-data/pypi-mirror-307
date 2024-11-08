from anthropic import Anthropic
from arm_rag.config import CONFIG


class Claude:
    def __init__(self, api_key, model=None, max_tokens=None):
        self.api_key = api_key
        self.client = Anthropic(api_key=self.api_key)
        if model:
            self.model = model
        else:
            self.model = CONFIG['claude']['model']
        if max_tokens:
            self.max_tokens = max_tokens
        else:
            self.max_tokens = CONFIG['claude']['max_tokens']
        self.user_prompt = CONFIG['claude']['prompt_template'][1]['user']
        self.system_prompt = CONFIG['claude']['prompt_template'][0]['system']
        self.temperature = CONFIG['claude']['temperature']
    
    
    def generate_response(self, input_text: str, context: str) -> str:
        # Format user prompt
        combined_prompt = self.user_prompt.format(
            context=context,
            question=input_text
        )
        
        print(combined_prompt)
        response = (
            self.client
            .messages
            .create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=self.system_prompt,
                messages=[
                        {
                            "role": "user",
                            "content": [
                                    {
                                        "type": "text",
                                        "text": combined_prompt
                                    }
                            ]

                        }
                ]
            )

        )
        return response.content[0].text
