from openai import OpenAI
from arm_rag.config import CONFIG



class Gpt:
    def __init__(self, api_key, model=None, max_tokens=None):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        if model:
            self.model = model
        else:
            self.model = CONFIG['gpt']['model']
        if max_tokens:
            self.max_tokens = max_tokens
        else:
            self.max_tokens = CONFIG['gpt']['max_tokens']

        self.user_prompt = CONFIG['gpt']['prompt_template'][1]['user']
        self.system_prompt = CONFIG['gpt']['prompt_template'][0]['system']
        self.temperature = CONFIG['gpt']['temperature']
    

    def generate_response(self, input_text: str, context: str) -> str:
        # Format user prompt
        combined_prompt = self.user_prompt.format(
            context=context,
            question=input_text
        )
        completion = (self.client
                      .chat
                      .completions
                      .create(
                          model=self.model,
                          max_tokens=self.max_tokens,
                          temperature=self.temperature,
                          messages=[
                              {"role": "system", "content": self.system_prompt},
                              {
                                  "role": "user",
                                  "content": combined_prompt
                              }
                            ]
                        )
                    )
        return completion.choices[0].message.content
