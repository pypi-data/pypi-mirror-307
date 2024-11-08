import torch
import numpy as np
from typing import Any
from transformers.pipelines import ArgumentHandler, pipeline
from PyGPTs.HuggingFace.base_objects import ObjectTypeKwargs
from PyVarTools.python_instances_tools import get_class_fields
from transformers import BaseImageProcessor, ModelCard, PreTrainedModel, PreTrainedTokenizer, PreTrainedTokenizerFast, PretrainedConfig, TFPreTrainedModel
#
#
#
#
class PipelineTypeKwargs(ObjectTypeKwargs):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
#
#
#
#
class TextGenerationPipelineKwargs(PipelineTypeKwargs):
	def __init__(
			self,
			args_parser: ArgumentHandler | None = None,
			batch_size: int | None = None,
			binary_output: bool | None = None,
			model_card: str | ModelCard | None = None,
			num_workers: int | None = None
	):
		super().__init__(
				args_parser=args_parser,
				batch_size=batch_size,
				binary_output=binary_output,
				model_card=model_card,
				num_workers=num_workers
		)
#
#
#
#
class HuggingFacePipelineSettings:
	def __init__(
			self,
			pipeline_class: Any = None,
			device: int | str | torch.device | None = None,
			device_map: int | str | torch.device | dict[str, int | str | torch.device] = None,
			feature_extractor: str | None = None,
			framework: str | None = None,
			image_processor: str | BaseImageProcessor | None = None,
			model: str | PreTrainedModel | TFPreTrainedModel | None = None,
			revision: str | None = None,
			task: str | None = None,
			token: str | bool | None = None,
			torch_dtype: str | torch.dtype = None,
			trust_remote_code: bool | None = None,
			use_fast: bool = None,
			config: str | PretrainedConfig | None = None,
			tokenizer: str | PreTrainedTokenizer | PreTrainedTokenizerFast | None = None,
			pipeline_type_kwargs: PipelineTypeKwargs = None
	):
		self.pipeline_class = pipeline_class
		self.config = config
		self.device = device
		self.device_map = device_map
		self.feature_extractor = feature_extractor
		self.framework = framework
		self.image_processor = image_processor
		self.model = model
		self.revision = revision
		self.task = task
		self.token = token
		self.tokenizer = tokenizer
		self.torch_dtype = torch_dtype
		self.trust_remote_code = trust_remote_code
		self.use_fast = use_fast
		#
		#
		#
		#
		if isinstance(pipeline_type_kwargs, PipelineTypeKwargs):
			for field, value in get_class_fields(pipeline_type_kwargs).items():
				if value is not None:
					setattr(self, field, value)
		elif pipeline_type_kwargs is not None:
			raise ValueError(
					"\"pipeline_type_kwargs\" must be of type PipelineTypeKwargs"
			)
#
#
#
#
class HuggingFacePipeline:
	def __init__(self, pipeline_settings: HuggingFacePipelineSettings):
		self.pipeline_ = pipeline(
				**{
					name: value for name, value in get_class_fields(pipeline_settings).items() if value is not None and name != "pipeline_type_kwargs"
				}
		)
	#
	#
	#
	#
	def pipe(
			self,
			inputs: np.ndarray | bytes | str | dict,
			max_length: int | None = None,
			max_new_tokens: int | None = None,
			return_timestamps: str | bool = None
	):
		return self.pipeline_(
				inputs,
				**{
					name: value for name, value in locals().items() if value is not None and name != "inputs"
				}
		)[0]["generated_text"][-1]["content"]
