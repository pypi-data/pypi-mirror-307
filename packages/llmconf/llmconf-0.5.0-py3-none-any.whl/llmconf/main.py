from dataclasses import dataclass, fields, is_dataclass

from .confs.openai_conf import OpenAIConf
from .confs.transf_conf import TransformersConf
from typing import Literal

@dataclass(kw_only=True, repr=False)
class LLMConf(OpenAIConf, TransformersConf):
    """Unified configuration for LLMs.

    - No data validation is performed.
    """

    # Shared
    system_message: str | None = None
    query: str | None = None
    backend: Literal["openai", "transformers"] | None = None

    def __post_init__(self):
        if self.backend is None:
            raise ValueError("backend is required.")
        if self.backend not in ["openai", "transformers"]:
            raise ValueError(f"Invalid backend: {self.backend}")

    def _to(self, to_class: object):
        if not is_dataclass(to_class):
            raise ValueError(f"{to_class.__name__} is not a dataclass.")

        from_fields = {f.name: getattr(self, f.name) for f in fields(self)}
        to_fields = {f.name: from_fields[f.name] for f in fields(to_class) if f.name in from_fields}
        return to_class(**to_fields)

    @property
    def openai(self) -> OpenAIConf:
        self.move(
            ["pretrained_model_name_or_path"],
            "model",
        )
        self.move(
            ["max_new_tokens", "max_tokens"],
            "max_completion_tokens",
        )
        if self.system_message is not None:
            self.messages = {"role": "system", "content": self.system_message}
        if self.query is not None:
            if self.messages is None:
                self.messages = []
            self.messages.append({"role": "user", "content": self.query})
        return self._to(OpenAIConf)

    @property
    def transformers(self) -> TransformersConf:
        self.move(
            ["model"],
            "pretrained_model_name_or_path",
        )
        self.move(
            ["max_completion_tokens", "max_tokens"],
            "max_new_tokens",
        )
        return self._to(TransformersConf)

    @property
    def load_params(self):
        raise AttributeError("load_params is not available for LLMConf.")

    @property
    def gene_params(self):
        raise AttributeError("gene_params is not available for LLMConf.")
