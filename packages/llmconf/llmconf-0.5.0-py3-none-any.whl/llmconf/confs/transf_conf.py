from dataclasses import dataclass

from .base_conf import BaseConf


@dataclass(kw_only=True, repr=False)
class TransformersConf(BaseConf):
    # Defined at: transformers.models.auto.auto_factory._BaseAutoModelClass.from_pretrained
    # Link: https://github.com/huggingface/transformers/blob/main/src/transformers/models/auto/auto_factory.py

    pretrained_model_name_or_path: str | None = None

    # Defined at: transformers.generation.configuration_utils.GenerationConfig.__init__
    # Link: https://github.com/huggingface/transformers/blob/main/src/transformers/generation/configuration_utils.py

    # Parameters that control the length of the output
    max_length: int | None = None
    max_new_tokens: int | None = None
    min_length: int | None = None
    min_new_tokens: int | None = None
    early_stopping: bool | str | None = None
    max_time: float | None = None
    stop_strings: list[str] | str | None = None

    # Parameters that control the generation strategy used
    do_sample: bool | None = None
    num_beams: int | None = None
    num_beam_groups: int | None = None
    penalty_alpha: float | None = None
    dola_layers: str | list[int] | None = None

    # Parameters that control the cache
    use_cache: bool | None = None
    cache_implementation: str | None = None
    cache_config: dict | None = None
    return_legacy_cache: bool | None = None

    # Parameters for manipulation of the model output logits
    temperature: float | None = None
    top_k: int | None = None
    top_p: float | None = None
    min_p: float | None = None
    typical_p: float | None = None
    epsilon_cutoff: float | None = None
    eta_cutoff: float | None = None
    diversity_penalty: float | None = None
    repetition_penalty: float | None = None
    encoder_repetition_penalty: float | None = None
    length_penalty: float | None = None
    no_repeat_ngram_size: int | None = None
    bad_words_ids: list[list[int]] | None = None
    force_words_ids: list[list[int]] | None = None
    renormalize_logits: bool | None = None
    constraints: list | None = None
    forced_bos_token_id: int | None = None
    forced_eos_token_id: int | list[int] | None = None
    remove_invalid_values: bool | None = None
    exponential_decay_length_penalty: tuple[int, float] | None = None
    suppress_tokens: list[int] | None = None
    begin_suppress_tokens: list[int] | None = None
    forced_decoder_ids: list[list[int]] | None = None
    sequence_bias: dict[tuple[int], float] | None = None
    token_healing: bool | None = None
    guidance_scale: float | None = None
    low_memory: bool | None = None
    watermarking_config: dict | None = None

    # Parameters that define the output variables of generate
    num_return_sequences: int | None = None
    output_attentions: bool | None = None
    output_hidden_states: bool | None = None
    output_scores: bool | None = None
    output_logits: bool | None = None
    return_dict_in_generate: bool | None = None

    # Special tokens that can be used at generation time
    pad_token_id: int | None = None
    bos_token_id: int | None = None
    eos_token_id: int | list[int] | None = None

    # Generation parameters exclusive to encoder-decoder models
    encoder_no_repeat_ngram_size: int | None = None
    decoder_start_token_id: int | list[int] | None = None

    # Generation parameters exclusive to assistant generation
    is_assistant: bool | None = None
    num_assistant_tokens: int | None = None
    num_assistant_tokens_schedule: str | None = None
    assistant_confidence_threshold: float | None = None
    prompt_lookup_num_tokens: int | None = None
    max_matching_ngram_size: int | None = None

    @property
    def load_params(self) -> dict:
        return self.dict_wo_none(
            {"pretrained_model_name_or_path": self.pretrained_model_name_or_path}
        )

    @property
    def gene_params(self) -> dict:
        return self.dict_wo_none(
            {
                "max_length": self.max_length,
                "max_new_tokens": self.max_new_tokens,
                "min_length": self.min_length,
                "min_new_tokens": self.min_new_tokens,
                "early_stopping": self.early_stopping,
                "max_time": self.max_time,
                "stop_strings": self.stop_strings,
                "do_sample": self.do_sample,
                "num_beams": self.num_beams,
                "num_beam_groups": self.num_beam_groups,
                "penalty_alpha": self.penalty_alpha,
                "dola_layers": self.dola_layers,
                "use_cache": self.use_cache,
                "cache_implementation": self.cache_implementation,
                "cache_config": self.cache_config,
                "return_legacy_cache": self.return_legacy_cache,
                "temperature": self.temperature,
                "top_k": self.top_k,
                "top_p": self.top_p,
                "min_p": self.min_p,
                "typical_p": self.typical_p,
                "epsilon_cutoff": self.epsilon_cutoff,
                "eta_cutoff": self.eta_cutoff,
                "diversity_penalty": self.diversity_penalty,
                "repetition_penalty": self.repetition_penalty,
                "encoder_repetition_penalty": self.encoder_repetition_penalty,
                "length_penalty": self.length_penalty,
                "no_repeat_ngram_size": self.no_repeat_ngram_size,
                "bad_words_ids": self.bad_words_ids,
                "force_words_ids": self.force_words_ids,
                "renormalize_logits": self.renormalize_logits,
                "constraints": self.constraints,
                "forced_bos_token_id": self.forced_bos_token_id,
                "forced_eos_token_id": self.forced_eos_token_id,
                "remove_invalid_values": self.remove_invalid_values,
                "exponential_decay_length_penalty": self.exponential_decay_length_penalty,
                "suppress_tokens": self.suppress_tokens,
                "begin_suppress_tokens": self.begin_suppress_tokens,
                "forced_decoder_ids": self.forced_decoder_ids,
                "sequence_bias": self.sequence_bias,
                "token_healing": self.token_healing,
                "guidance_scale": self.guidance_scale,
                "low_memory": self.low_memory,
                "watermarking_config": self.watermarking_config,
                "num_return_sequences": self.num_return_sequences,
                "output_attentions": self.output_attentions,
                "output_hidden_states": self.output_hidden_states,
                "output_scores": self.output_scores,
                "output_logits": self.output_logits,
                "return_dict_in_generate": self.return_dict_in_generate,
                "pad_token_id": self.pad_token_id,
                "bos_token_id": self.bos_token_id,
                "eos_token_id": self.eos_token_id,
                "encoder_no_repeat_ngram_size": self.encoder_no_repeat_ngram_size,
                "decoder_start_token_id": self.decoder_start_token_id,
                "is_assistant": self.is_assistant,
                "num_assistant_tokens": self.num_assistant_tokens,
                "num_assistant_tokens_schedule": self.num_assistant_tokens_schedule,
                "assistant_confidence_threshold": self.assistant_confidence_threshold,
                "prompt_lookup_num_tokens": self.prompt_lookup_num_tokens,
                "max_matching_ngram_size": self.max_matching_ngram_size,
            }
        )
