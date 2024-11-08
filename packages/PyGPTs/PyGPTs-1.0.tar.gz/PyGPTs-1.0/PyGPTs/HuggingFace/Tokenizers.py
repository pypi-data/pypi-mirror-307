import torch
from os import PathLike
from PyGPTs.HuggingFace.base_objects import ObjectTypeKwargs
from PyVarTools.python_instances_tools import get_class_fields
from transformers import AutoTokenizer, PreTrainedTokenizer, PretrainedConfig
#
#
#
#
class TokenizerTypeKwargs(ObjectTypeKwargs):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
#
#
#
#
class HuggingFaceTokenizerSettings:
	def __init__(
			self,
			pretrained_model_name_or_path: str | PathLike,
			cache_dir: str | PathLike = None,
			config: PretrainedConfig = None,
			force_download: bool = None,
			proxies: dict[str, str] = None,
			sub_folder: str = None,
			tokenizer_type: str = None,
			torch_dtype: str | torch.dtype = None,
			trust_remote_code: bool = None,
			token: str = None,
			use_fast: bool = None,
			tokenizer_type_kwargs: TokenizerTypeKwargs = None
	):
		self.pretrained_model_name_or_path = pretrained_model_name_or_path
		self.cache_dir = cache_dir
		self.config = config
		self.force_download = force_download
		self.proxies = proxies
		self.sub_folder = sub_folder
		self.token = token
		self.torch_dtype = torch_dtype
		self.tokenizer_type = tokenizer_type
		self.trust_remote_code = trust_remote_code
		self.use_fast = use_fast
		#
		#
		#
		#
		if isinstance(tokenizer_type_kwargs, TokenizerTypeKwargs):
			for field, value in get_class_fields(tokenizer_type_kwargs).items():
				if value is not None:
					setattr(self, field, value)
		elif tokenizer_type_kwargs is not None:
			raise ValueError(
					"\"tokenizer_type_kwargs\" must be of type TokenizerTypeKwargs"
			)
#
#
#
#
class HuggingFaceTokenizer:
	def __init__(self, tokenizer_settings: HuggingFaceTokenizerSettings):
		self.tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(
				**{
					name: value for name, value in get_class_fields(tokenizer_settings).items() if value is not None
				}
		)
