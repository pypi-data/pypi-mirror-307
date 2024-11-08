import torch
import numpy as np
from typing import Any
from os import PathLike
from transformers import BaseImageProcessor, PretrainedConfig
from PyVarTools.python_instances_tools import get_function_parameters
from transformers.utils.quantization_config import QuantizationConfigMixin
from PyGPTs.HuggingFace.Models import HuggingFaceModel, HuggingFaceModelSettings, ModelTypeKwargs
from PyGPTs.HuggingFace.Pipelines import HuggingFacePipeline, HuggingFacePipelineSettings, PipelineTypeKwargs
from PyGPTs.HuggingFace.Tokenizers import HuggingFaceTokenizer, HuggingFaceTokenizerSettings, TokenizerTypeKwargs
#
#
#
#
class HuggingFaceTransformerSettings:
	def __init__(
			self,
			pretrained_model_name_or_path: str | PathLike,
			model_class: Any,
			pipeline_class: Any = None,
			attn_implementation: str = None,
			cache_dir: str | PathLike = None,
			code_revision: str = None,
			config: PretrainedConfig = None,
			device: int | str | torch.device | None = None,
			device_map: int | str | torch.device | dict[str, int | str | torch.device] = None,
			feature_extractor: str | None = None,
			force_download: bool = False,
			from_flax: bool = None,
			from_tf: bool = None,
			framework: str | None = None,
			image_processor: str | BaseImageProcessor | None = None,
			ignore_mismatched_sizes: bool = None,
			local_files_only: bool = None,
			low_cpu_mem_usage: bool = None,
			max_memory: dict = None,
			mirror: str = None,
			offload_buffers: bool = None,
			offload_folder: str | PathLike = None,
			offload_state_dict: bool = None,
			output_loading_info: bool = None,
			proxies: dict[str, str] = None,
			quantization_config: QuantizationConfigMixin | dict = None,
			revision: str = None,
			state_dict: dict[str, str] = None,
			sub_folder: str = None,
			task: str | None = None,
			token: str = None,
			torch_dtype: str | torch.dtype = None,
			trust_remote_code: bool = None,
			tokenizer_type: str = None,
			use_fast: bool = None,
			use_safetensors: bool = None,
			variant: str = None,
			_fast_init: bool = None,
			model_type_kwargs: ModelTypeKwargs = None,
			tokenizer_type_kwargs: TokenizerTypeKwargs = None,
			pipeline_type_kwargs: PipelineTypeKwargs = None
	):
		parameters = locals()
		self.model_settings = HuggingFaceModelSettings(
				**{
					name: parameters[name] for name in get_function_parameters(
							function_=HuggingFaceModelSettings.__init__,
							excluding_parameters=["self"]
					).keys()
				}
		)
		self.tokenizer_settings = HuggingFaceTokenizerSettings(
				**{
					name: parameters[name] for name in get_function_parameters(
							function_=HuggingFaceTokenizerSettings.__init__,
							excluding_parameters=["self"]
					).keys()
				}
		)
		self.pipeline_settings = HuggingFacePipelineSettings(
				**{
					name: parameters[name] for name in get_function_parameters(
							function_=HuggingFacePipelineSettings.__init__,
							excluding_parameters=["self", "model", "tokenizer"]
					).keys()
				}
		)
#
#
#
#
class HuggingFaceTransformer:
	def __init__(
			self,
			huggingface_transformer_settings: HuggingFaceTransformerSettings
	):
		self.model = HuggingFaceModel(
				model_settings=huggingface_transformer_settings.model_settings
		)
		self.tokenizer = HuggingFaceTokenizer(
				tokenizer_settings=huggingface_transformer_settings.tokenizer_settings
		)
		huggingface_transformer_settings.pipeline_settings.model = self.model.model
		huggingface_transformer_settings.pipeline_settings.tokenizer = self.tokenizer.tokenizer
		self.pipeline = HuggingFacePipeline(
				pipeline_settings=huggingface_transformer_settings.pipeline_settings
		)
	#
	#
	#
	#
	def generate_content(
			self,
			inputs: np.ndarray | bytes | str | dict,
			max_length: int | None = None,
			max_new_tokens: int | None = None,
			return_timestamps: str | bool = None
	):
		return self.pipeline.pipe(
				inputs=inputs,
				max_length=max_length,
				max_new_tokens=max_new_tokens,
				return_timestamps=return_timestamps
		)
