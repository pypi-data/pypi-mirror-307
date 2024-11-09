import os

from dataclasses import dataclass, field

from .base_conf import BaseConf


@dataclass(kw_only=True, repr=False)
class OpenAIConf(BaseConf):
    # Defined at: openai._clinet.OpenAI.__init__
    # Link: https://github.com/openai/openai-python/blob/main/src/openai/_client.py

    api_key: str | None = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", None))
    organization: str | None = field(default_factory=lambda: os.getenv("OPENAI_ORG_ID", None))
    project: str | None = field(default_factory=lambda: os.getenv("OPENAI_PROJECT_ID", None))
    base_url: str | None = field(default_factory=lambda: os.getenv("OPENAI_BASE_URL", None))
    timeout: float | None = None
    max_retries: int | None = None

    # Defined at: openai.resources.chat.completions.Completions.create
    # Link: https://github.com/openai/openai-python/blob/main/src/openai/resources/chat/completions.py

    messages: list[dict[str, str]] | None = None
    model: str | None = None
    frequency_penalty: float | None = None
    logit_bias: dict[str, int] | None = None
    logprobs: bool | None = None
    max_completion_tokens: int | None = None
    max_tokens: int | None = None
    n: int | None = None
    presence_penalty: float | None = None
    seed: int | None = None
    temperature: float | None = None
    top_logprobs: int | None = None
    top_p: float | None = None
    user: str | None = None

    @property
    def load_params(self):
        return self.dict_wo_none(
            {
                "api_key": self.api_key,
                "organization": self.organization,
                "project": self.project,
                "base_url": self.base_url,
                "timeout": self.timeout,
                "max_retries": self.max_retries,
            }
        )

    @property
    def gene_params(self):
        return self.dict_wo_none(
            {
                "messages": self.messages,
                "model": self.model,
                "frequency_penalty": self.frequency_penalty,
                "logit_bias": self.logit_bias,
                "logprobs": self.logprobs,
                "max_completion_tokens": self.max_completion_tokens,
                "max_tokens": self.max_tokens,
                "n": self.n,
                "presence_penalty": self.presence_penalty,
                "seed": self.seed,
                "temperature": self.temperature,
                "top_logprobs": self.top_logprobs,
                "top_p": self.top_p,
                "user": self.user,
            }
        )
