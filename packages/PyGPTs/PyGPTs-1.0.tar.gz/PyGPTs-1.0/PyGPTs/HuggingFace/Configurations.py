from typing import Any
from os import PathLike
from transformers import PretrainedConfig
from PyVarTools.python_instances_tools import get_class_fields
#
#
#
#
class HuggingFaceTensorFlowSpecificConfigSettings:
	def __init__(self, tf_legacy_loss: bool = None, use_bfloat16: bool = None):
		self.tf_legacy_loss = tf_legacy_loss
		self.use_bfloat16 = use_bfloat16
#
#
#
#
class HuggingFacePyTorchSpecificConfigSettings:
	def __init__(
			self,
			tie_word_embeddings: bool = None,
			torchscript: bool = None,
			torch_dtype: str = None
	):
		self.tie_word_embeddings = tie_word_embeddings
		self.torchscript = torchscript
		self.torch_dtype = torch_dtype
#
#
#
#
class HuggingFaceConfigSettings:
	def __init__(
			self,
			pretrained_model_name_or_path: str | PathLike,
			add_cross_attention: bool = None,
			architectures: list[str] = None,
			bad_words_ids: list[int] = None,
			chunk_size_feed_forward: int = None,
			cross_attention_hidden_size: bool = None,
			diversity_penalty: float = None,
			do_sample: bool = None,
			early_stopping: bool = None,
			encoder_no_repeat_ngram_size: int = None,
			finetuning_task: str = None,
			forced_bos_token_id: int = None,
			forced_eos_token_id: int | list[int] = None,
			id2label: dict[int, str] = None,
			is_decoder: bool = None,
			is_encoder_decoder: bool = None,
			label2id: dict[str, int] = None,
			length_penalty: float = None,
			max_length: int = None,
			min_length: int = None,
			no_repeat_ngram_size: int = None,
			num_beam_groups: int = None,
			num_beams: int = None,
			num_labels: int = None,
			num_return_sequences: int = None,
			output_attentions: bool = None,
			output_hidden_states: bool = None,
			output_scores: bool = None,
			problem_type: str = None,
			prune_heads: dict[int, list[int]] = None,
			remove_invalid_values: bool = None,
			repetition_penalty: float = None,
			return_dict: bool = None,
			return_dict_in_generate: bool = None,
			task_specific_params: dict[str, Any] = None,
			temperature: float = None,
			tie_encoder_decoder: bool = None,
			top_k: int = None,
			top_p: float = None,
			typical_p: float = None,
			specific_config_settings: HuggingFacePyTorchSpecificConfigSettings | HuggingFaceTensorFlowSpecificConfigSettings = None
	):
		self.pretrained_model_name_or_path = pretrained_model_name_or_path
		self.add_cross_attention = add_cross_attention
		self.architectures = architectures
		self.bad_words_ids = bad_words_ids
		self.chunk_size_feed_forward = chunk_size_feed_forward
		self.cross_attention_hidden_size = cross_attention_hidden_size
		self.diversity_penalty = diversity_penalty
		self.do_sample = do_sample
		self.early_stopping = early_stopping
		self.encoder_no_repeat_ngram_size = encoder_no_repeat_ngram_size
		self.finetuning_task = finetuning_task
		self.forced_bos_token_id = forced_bos_token_id
		self.forced_eos_token_id = forced_eos_token_id
		self.id2label = id2label
		self.is_decoder = is_decoder
		self.is_encoder_decoder = is_encoder_decoder
		self.label2id = label2id
		self.length_penalty = length_penalty
		self.max_length = max_length
		self.min_length = min_length
		self.no_repeat_ngram_size = no_repeat_ngram_size
		self.num_beam_groups = num_beam_groups
		self.num_beams = num_beams
		self.num_labels = num_labels
		self.num_return_sequences = num_return_sequences
		self.output_attentions = output_attentions
		self.output_hidden_states = output_hidden_states
		self.output_scores = output_scores
		self.problem_type = problem_type
		self.prune_heads = prune_heads
		self.remove_invalid_values = remove_invalid_values
		self.repetition_penalty = repetition_penalty
		self.return_dict = return_dict
		self.return_dict_in_generate = return_dict_in_generate
		self.task_specific_params = task_specific_params
		self.temperature = temperature
		self.tie_encoder_decoder = tie_encoder_decoder
		self.top_k = top_k
		self.top_p = top_p
		self.typical_p = typical_p
		#
		#
		#
		#
		if isinstance(
				specific_config_settings,
				(
						HuggingFacePyTorchSpecificConfigSettings,
						HuggingFaceTensorFlowSpecificConfigSettings
				)
		):
			for field, value in get_class_fields(specific_config_settings).items():
				if value is not None:
					setattr(self, field, value)
		elif specific_config_settings is not None:
			raise ValueError(
					"\"specific_config_settings\" must be of type HuggingFacePyTorchSpecificConfigSettings or HuggingFaceTensorFlowSpecificConfigSettings"
			)
#
#
#
#
class HuggingFaceConfig:
	def __init__(self, generation_config_settings: HuggingFaceConfigSettings):
		self.config = PretrainedConfig.from_pretrained(
				**{
					name: value for name, value in get_class_fields(generation_config_settings).items() if value is not None
				}
		)
