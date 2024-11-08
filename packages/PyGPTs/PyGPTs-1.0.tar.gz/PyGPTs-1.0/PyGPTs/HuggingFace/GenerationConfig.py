from os import PathLike
from PyVarTools.python_instances_tools import get_class_fields
from transformers import Constraint, GenerationConfig, WatermarkingConfig
#
#
#
#
class HuggingFaceGenerationTokensUsedSettings:
	def __init__(
			self,
			bos_token_id: int = None,
			eos_token_id: int | list[int] = None,
			pad_token_id: int = None
	):
		self.bos_token_id = bos_token_id
		self.eos_token_id = eos_token_id
		self.pad_token_id = pad_token_id
#
#
#
#
class HuggingFaceGenerationStrategySettings:
	def __init__(
			self,
			do_sample: bool = None,
			num_beam_groups: int = None,
			num_beams: int = None,
			penalty_alpha: float = None,
			use_cache: bool = None
	):
		self.do_sample = do_sample
		self.num_beam_groups = num_beam_groups
		self.num_beams = num_beams
		self.penalty_alpha = penalty_alpha
		self.use_cache = use_cache
#
#
#
#
class HuggingFaceGenerationOutputVariablesSettings:
	def __init__(
			self,
			num_return_sequences: int = None,
			output_attentions: bool = None,
			output_hidden_states: bool = None,
			output_scores: bool = None,
			output_logits: bool = None,
			return_dict_in_generate: bool = None
	):
		self.num_return_sequences = num_return_sequences
		self.output_attentions = output_attentions
		self.output_hidden_states = output_hidden_states
		self.output_scores = output_scores
		self.output_logits = output_logits
		self.return_dict_in_generate = return_dict_in_generate
#
#
#
#
class HuggingFaceGenerationOutputSettings:
	def __init__(
			self,
			early_stopping: bool = None,
			max_length: int = None,
			max_new_tokens: int = None,
			max_time: float = None,
			min_length: int = None,
			min_new_tokens: int = None,
			stop_strings: str | list[str] = None
	):
		self.early_stopping = early_stopping
		self.max_length = max_length
		self.max_new_tokens = max_new_tokens
		self.max_time = max_time
		self.min_length = min_length
		self.min_new_tokens = min_new_tokens
		self.stop_strings = stop_strings
#
#
#
#
class HuggingFaceGenerationOutputLogitsSettings:
	def __init__(
			self,
			bad_words_ids: list[list[int]] = None,
			begin_suppress_tokens: list[int] = None,
			constraints: list[Constraint] = None,
			diversity_penalty: float = None,
			encoder_repetition_penalty: float = None,
			epsilon_cutoff: float = None,
			eta_cutoff: float = None,
			exponential_decay_length_penalty: tuple[int, float] = None,
			force_words_ids: list[list[int]] = None,
			forced_bos_token_id: int = None,
			forced_decoder_ids: list[list[int]] = None,
			forced_eos_token_id: int | list[int] = None,
			guidance_scale: float = None,
			length_penalty: float = None,
			low_memory: float = None,
			min_p: float = None,
			no_repeat_ngram_size: int = None,
			remove_invalid_values: bool = None,
			renormalize_logits: bool = None,
			repetition_penalty: float = None,
			sequence_bias: dict[tuple[int], float] = None,
			suppress_tokens: list[int] = None,
			temperature: float = None,
			token_healing: bool = None,
			top_k: int = None,
			top_p: float = None,
			typical_p: float = None,
			watermarking_config: WatermarkingConfig | dict = None
	):
		self.bad_words_ids = bad_words_ids
		self.begin_suppress_tokens = begin_suppress_tokens
		self.constraints = constraints
		self.diversity_penalty = diversity_penalty
		self.encoder_repetition_penalty = encoder_repetition_penalty
		self.epsilon_cutoff = epsilon_cutoff
		self.eta_cutoff = eta_cutoff
		self.exponential_decay_length_penalty = exponential_decay_length_penalty
		self.force_words_ids = force_words_ids
		self.forced_bos_token_id = forced_bos_token_id
		self.forced_decoder_ids = forced_decoder_ids
		self.forced_eos_token_id = forced_eos_token_id
		self.guidance_scale = guidance_scale
		self.length_penalty = length_penalty
		self.low_memory = low_memory
		self.min_p = min_p
		self.no_repeat_ngram_size = no_repeat_ngram_size
		self.remove_invalid_values = remove_invalid_values
		self.renormalize_logits = renormalize_logits
		self.repetition_penalty = repetition_penalty
		self.sequence_bias = sequence_bias
		self.suppress_tokens = suppress_tokens
		self.temperature = temperature
		self.token_healing = token_healing
		self.top_k = top_k
		self.top_p = top_p
		self.typical_p = typical_p
		self.watermarking_config = watermarking_config
#
#
#
#
class HuggingFaceGenerationConfigSettings:
	def __init__(
			self,
			pretrained_model_name_or_path: str | PathLike,
			config_file_name: str | PathLike = None,
			cache_dir: str | PathLike = None,
			force_download: bool = None, proxies: dict[str, str] = None, token: str | bool = None, return_unused_kwargs: bool = None, sub_folder: str = None, generation_output_logits_settings: HuggingFaceGenerationOutputLogitsSettings = None,
			generation_output_settings: HuggingFaceGenerationOutputSettings = None,
			generation_output_variables_settings: HuggingFaceGenerationOutputVariablesSettings = None,
			generation_strategy_settings: HuggingFaceGenerationStrategySettings = None,
			generation_tokens_used_settings: HuggingFaceGenerationTokensUsedSettings = None
	):
		self.pretrained_model_name_or_path = pretrained_model_name_or_path
		self.config_file_name = config_file_name
		self.cache_dir = cache_dir
		self.force_download = force_download
		self.proxies = proxies
		self.token = token
		self.return_unused_kwargs = return_unused_kwargs
		self.sub_folder = sub_folder
		#
		#
		#
		#
		if generation_output_logits_settings is not None:
			for name, value in get_class_fields(generation_output_logits_settings).items():
				if value is not None:
					setattr(self, name, value)
		#
		#
		#
		#
		if generation_output_settings is not None:
			for name, value in get_class_fields(generation_output_settings).items():
				if value is not None:
					setattr(self, name, value)
		#
		#
		#
		#
		if generation_output_variables_settings is not None:
			for name, value in get_class_fields(generation_output_variables_settings).items():
				if value is not None:
					setattr(self, name, value)
		#
		#
		#
		#
		if generation_strategy_settings is not None:
			for name, value in get_class_fields(generation_strategy_settings).items():
				if value is not None:
					setattr(self, name, value)
		#
		#
		#
		#
		if generation_tokens_used_settings is not None:
			for name, value in get_class_fields(generation_tokens_used_settings).items():
				if value is not None:
					setattr(self, name, value)
#
#
#
#
class HuggingFaceGenerationConfig:
	def __init__(self, generation_config_settings: HuggingFaceGenerationConfigSettings):
		self.generation_config = GenerationConfig.from_pretrained(
				**{
					name: value for name, value in get_class_fields(generation_config_settings).items() if value is not None
				}
		)
