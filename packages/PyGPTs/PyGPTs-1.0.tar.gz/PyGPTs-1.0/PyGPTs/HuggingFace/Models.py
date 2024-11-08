import torch
from typing import Any
from os import PathLike
from transformers import PreTrainedModel, PretrainedConfig
from PyGPTs.HuggingFace.base_objects import ObjectTypeKwargs
from PyVarTools.python_instances_tools import get_class_fields
from transformers.utils.quantization_config import QuantizationConfigMixin
#
#
#
#
class ModelTypeKwargs(ObjectTypeKwargs):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
#
#
#
#
class HuggingFaceModelSettings:
	def __init__(
			self,
			pretrained_model_name_or_path: str | PathLike,
			model_class: Any,
			attn_implementation: str = None,
			cache_dir: str | PathLike = None,
			code_revision: str = None,
			config: PretrainedConfig = None,
			device_map: int | str | torch.device | dict[str, int | str | torch.device] = None,
			force_download: bool = False,
			from_flax: bool = None,
			from_tf: bool = None,
			ignore_mismatched_sizes: bool = None,
			local_files_only: bool = None,
			low_cpu_mem_usage: bool = None,
			max_memory: dict = None,
			mirror: str = None,
			offload_buffers: bool = None,
			offload_folder: str | PathLike = None,
			output_loading_info: bool = None,
			offload_state_dict: bool = None,
			proxies: dict[str, str] = None,
			quantization_config: QuantizationConfigMixin | dict = None,
			revision: str = None,
			state_dict: dict[str, str] = None,
			sub_folder: str = None,
			token: str = None,
			torch_dtype: str | torch.dtype = None,
			trust_remote_code: bool = None,
			use_safetensors: bool = None,
			variant: str = None,
			_fast_init: bool = None,
			model_type_kwargs: ModelTypeKwargs = None
	):
		self.pretrained_model_name_or_path = pretrained_model_name_or_path
		self.model_class = model_class
		self.attn_implementation = attn_implementation
		self.cache_dir = cache_dir
		self.code_revision = code_revision
		self.config = config
		self.device_map = device_map
		self.force_download = force_download
		self.from_flax = from_flax
		self.from_tf = from_tf
		self.ignore_mismatched_sizes = ignore_mismatched_sizes
		self.local_files_only = local_files_only
		self.low_cpu_mem_usage = low_cpu_mem_usage
		self.max_memory = max_memory
		self.mirror = mirror
		self.offload_buffers = offload_buffers
		self.offload_folder = offload_folder
		self.output_loading_info = output_loading_info
		self.offload_state_dict = offload_state_dict
		self.proxies = proxies
		self.quantization_config = quantization_config
		self.revision = revision
		self.state_dict = state_dict
		self.sub_folder = sub_folder
		self.token = token
		self.torch_dtype = torch_dtype
		self.trust_remote_code = trust_remote_code
		self.use_safetensors = use_safetensors
		self.variant = variant
		self._fast_init = _fast_init
		#
		#
		#
		#
		if isinstance(model_type_kwargs, ModelTypeKwargs):
			for field, value in get_class_fields(model_type_kwargs).items():
				if value is not None:
					setattr(self, field, value)
		elif model_type_kwargs is not None:
			raise ValueError("\"model_type_kwargs\" must be of type ModelTypeKwargs")
#
#
#
#
class HuggingFaceModel:
	def __init__(self, model_settings: HuggingFaceModelSettings):
		self.model: PreTrainedModel = model_settings.model_class.from_pretrained(
				**{
					name: value for name, value in get_class_fields(model_settings).items() if value is not None and name != "model_class"
				}
		)
