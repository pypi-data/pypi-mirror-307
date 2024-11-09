"""Note: This interface is not stable and may change in the future.

Examples:

```python
from src.llmconf import LLMConf, SimpleLLM

conf = LLMConf(
    backend="transformers",
    pretrained_model_name_or_path="gpt2",
    max_new_tokens=10,
)

llm = SimpleLLM(conf)
response = llm.generate("Hello, world!")
print(response)
print(llm.conf)
```
"""
from openai import OpenAI
from . import LLMConf
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class SimpleLLM:
    def __init__(self, conf: LLMConf):
        if conf.backend == "openai":
            self.conf = conf.openai
            self.client = OpenAI(**self.conf.load_params)
        elif conf.backend == "transformers":
            self.conf = conf.transformers
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.tokenizer = AutoTokenizer.from_pretrained(**{**self.conf.load_params, "trust_remote_code": True})
            self.model = AutoModelForCausalLM.from_pretrained(**{**self.conf.load_params, "trust_remote_code": True}).to(device)
    
    def generate(self, prompt: str):
        if self.conf.backend == "openai":
            chat_completion = self.client.chat.completions.create(
                **{**self.conf.gene_params,
                "messages":[*self.conf.messages, {"role": "user", "content": prompt}]},
            )
            response = chat_completion.choices[0].message.content
            return response
        elif self.conf.backend == "transformers":
            input_ids = self.tokenizer.encode(prompt, return_tensors="pt").to(self.model.device)
            output_ids = self.model.generate(input_ids, **self.conf.gene_params)[0]
            response = self.tokenizer.decode(
                output_ids[len(input_ids[0]) - len(output_ids) :], skip_special_tokens=True
            )
            return response
