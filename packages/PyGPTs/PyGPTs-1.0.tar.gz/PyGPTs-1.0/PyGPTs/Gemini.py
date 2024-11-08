from pytz import timezone
from time import sleep, time
from datetime import datetime
import google.generativeai as genai
from google.generativeai import ChatSession, GenerationConfig, GenerativeModel
from google.generativeai.types import HarmBlockThreshold, HarmCategory, RequestOptions
#
#
#
#
class GeminiLimits:
	request_per_day = {"gemini-1.5-pro": 50, "gemini-1.5-flash": 1000, "gemini-1.0-pro": 1000}
	request_per_minute = {"gemini-1.5-pro": 2, "gemini-1.5-flash": 10, "gemini-1.0-pro": 10}
	tokens_per_minute = {
		"gemini-1.5-pro": 32 * 10 ** 3,
		"gemini-1.5-flash": 10 ** 6,
		"gemini-1.0-pro": 32 * 10 ** 3
	}
#
#
#
#
class GeminiModels:
	gemini_1_5_pro = "gemini-1.5-pro"
	gemini_1_5_flash = "gemini-1.5-flash"
	gemini_1_0_pro = "gemini-1.0-pro"
#
#
#
#
class GeminiSettings:
	#
	#
	#
	#
	def __init__(
			self,
			api_key: str,
			model_name: str = GeminiModels.gemini_1_5_flash,
			safety_settings: dict[HarmCategory, HarmBlockThreshold] = None,
			generation_config: GenerationConfig = GenerationConfig(
					candidate_count=1,
					temperature=0.7,
					top_p=0.5,
					top_k=40,
					response_mime_type="text/plain"
			),
			start_day: datetime = None,
			request_per_day_used: int = 0,
			request_per_day_limit: int = None,
			request_per_minute_limit: int = None,
			tokens_per_minute_limit: int = None,
			raise_error_on_limit: bool = True
	):
		if safety_settings is None:
			safety_settings = {
				HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
				HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
				HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
				HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
			}
		#
		#
		#
		#
		self.api_key = api_key
		self.model_name = model_name
		self.safety_settings = safety_settings
		self.generation_config = generation_config
		self.raise_error_on_limit = raise_error_on_limit
		self.request_per_day_used = request_per_day_used
		#
		#
		#
		#
		if start_day is None:
			current_date = datetime.now(tz=timezone("America/New_York"))
		else:
			current_date = start_day.astimezone(timezone("America/New_York"))
		#
		#
		#
		#
		self.start_day = datetime(
				year=current_date.year,
				month=current_date.month,
				day=current_date.day,
				tzinfo=current_date.tzinfo
		)
		#
		#
		#
		#
		if request_per_day_limit is None:
			self.request_per_day_limit = GeminiLimits.request_per_day[model_name]
		else:
			self.request_per_day_limit = request_per_day_limit
		#
		#
		#
		#
		if request_per_minute_limit is None:
			self.request_per_minute_limit = GeminiLimits.request_per_minute[model_name]
		else:
			self.request_per_minute_limit = request_per_minute_limit
		#
		#
		#
		#
		if tokens_per_minute_limit is None:
			self.tokens_per_minute_limit = GeminiLimits.tokens_per_minute[model_name]
		else:
			self.tokens_per_minute_limit = tokens_per_minute_limit
#
#
#
#
class GeminiNoUsefulModelsException(Exception):
	#
	#
	#
	#
	def __init__(self):
		super().__init__("All Gemini limits reached")
#
#
#
#
class GeminiMinuteLimitException(Exception):
	#
	#
	#
	#
	def __init__(self):
		super().__init__("Minute limit reached")
#
#
#
#
class GeminiDayLimitException(Exception):
	#
	#
	#
	#
	def __init__(self):
		super().__init__("Day limit reached")
#
#
#
#
class GeminiLimiter:
	#
	#
	#
	#
	def __init__(
			self,
			start_day: datetime,
			request_per_day_used: int,
			request_per_day_limit: int,
			request_per_minute_limit: int,
			tokens_per_minute_limit: int,
			raise_error_on_limit: bool = True
	):
		self.start_day = start_day
		self.request_per_day_limit = request_per_day_limit
		self.request_per_minute_limit = request_per_minute_limit
		self.tokens_per_minute_limit = tokens_per_minute_limit
		self.raise_error_on_limit = raise_error_on_limit
		self.request_per_day_used = request_per_day_used
		self.request_per_minute_used = 0
		self.tokens_per_minute_used = 0
		self.start_time = time()
	#
	#
	#
	#
	def close_minute_limit(self):
		self.request_per_minute_used = self.request_per_minute_limit
		self.tokens_per_minute_used = self.tokens_per_minute_limit
	#
	#
	#
	#
	def close_day_limit(self):
		self.request_per_day_used = self.request_per_day_limit
	#
	#
	#
	#
	def check_limits(self, last_tokens: int):
		elapsed_time = time() - self.start_time

		if elapsed_time < 60:
			if self.request_per_day_used > self.request_per_day_limit:
				if datetime.now(tz=timezone("America/New_York")).day != self.start_day.day:
					self.request_per_day_used = 1

					current_date = datetime.now(tz=timezone("America/New_York"))
					self.start_day = datetime(
							year=current_date.year,
							month=current_date.month,
							day=current_date.day,
							tzinfo=current_date.tzinfo
					)
				else:
					raise GeminiDayLimitException()
			elif datetime.now(tz=timezone("America/New_York")).day != self.start_day.day:
				self.request_per_day_used = 1

				current_date = datetime.now(tz=timezone("America/New_York"))
				self.start_day = datetime(
						year=current_date.year,
						month=current_date.month,
						day=current_date.day,
						tzinfo=current_date.tzinfo
				)
			elif self.request_per_minute_used > self.request_per_minute_limit or self.tokens_per_minute_used > self.tokens_per_minute_limit:
				if self.raise_error_on_limit:
					raise GeminiMinuteLimitException()
				else:
					sleep(60 - elapsed_time)

					self.request_per_minute_used = 1
					self.tokens_per_minute_used = last_tokens

					self.start_time = time()
		else:
			self.request_per_minute_used = 1
			self.tokens_per_minute_used = last_tokens

			self.start_time = time()
	#
	#
	#
	#
	def add_data(self, tokens: int):
		self.request_per_day_used += 1
		self.request_per_minute_used += 1
		self.tokens_per_minute_used += tokens

		self.check_limits(tokens)
#
#
#
#
class Gemini:
	#
	#
	#
	#
	def __init__(self, gemini_settings: GeminiSettings):
		genai.configure(api_key=gemini_settings.api_key)
		#
		#
		#
		#
		self.api_key = gemini_settings.api_key
		self.model_name = gemini_settings.model_name
		#
		#
		#
		#
		self.model = GenerativeModel(
				model_name=gemini_settings.model_name,
				safety_settings=gemini_settings.safety_settings,
				generation_config=gemini_settings.generation_config
		)
		#
		#
		#
		#
		self.limiter = GeminiLimiter(
				start_day=gemini_settings.start_day,
				request_per_day_used=gemini_settings.request_per_day_used,
				request_per_day_limit=gemini_settings.request_per_day_limit,
				request_per_minute_limit=gemini_settings.request_per_minute_limit,
				tokens_per_minute_limit=gemini_settings.tokens_per_minute_limit,
				raise_error_on_limit=gemini_settings.raise_error_on_limit
		)
		#
		#
		#
		#
		self.chats: list[ChatSession] = []
	#
	#
	#
	#
	def start_chat(self):
		self.chats.append(self.model.start_chat())
	#
	#
	#
	#
	def send_message(
			self,
			message: str,
			stream: bool = False,
			request_options: RequestOptions = RequestOptions(),
			chat_index: int = -1
	):
		return self.chats[chat_index].send_message(content=message, stream=stream, request_options=request_options)
	#
	#
	#
	#
	def get_model_name(self):
		return self.model_name
	#
	#
	#
	#
	def get_minute_limits_used(self):
		return {
			"used_requests": self.limiter.request_per_minute_used,
			"used_tokens": self.limiter.tokens_per_minute_used,
			"requests_limit": self.limiter.request_per_minute_limit,
			"tokens_limit": self.limiter.tokens_per_minute_limit
		}
	#
	#
	#
	#
	def get_day_limits_used(self):
		return {
			"used_requests": self.limiter.request_per_day_used,
			"requests_limit": self.limiter.request_per_day_limit,
			"date": self.limiter.start_day
		}
	#
	#
	#
	#
	def get_current_limit_day(self):
		return self.limiter.start_day
	#
	#
	#
	#
	def get_api_key(self):
		return self.api_key
	#
	#
	#
	#
	def generate_content(
			self,
			message: str,
			stream: bool = False,
			request_options: RequestOptions = RequestOptions()
	):
		self.limiter.add_data(
				self.model.count_tokens(contents=message, request_options=request_options).total_tokens
		)

		return self.model.generate_content(contents=message, stream=stream, request_options=request_options)
	#
	#
	#
	#
	def close_minute_limit(self):
		self.limiter.close_minute_limit()
	#
	#
	#
	#
	def close_day_limit(self):
		self.limiter.close_day_limit()
	#
	#
	#
	#
	def close_chat(self, chat_index: int = -1):
		self.chats.pop(chat_index)
#
#
#
#
class GeminiManager:
	#
	#
	#
	#
	def __init__(self, geminis_settings: list[GeminiSettings]):
		self.models_settings = geminis_settings
		self.current_model_index = self.get_lowest_useful_model_index()
		#
		#
		#
		#
		self.current_model = Gemini(self.models_settings[self.current_model_index])
	#
	#
	#
	#
	def check_models_limits(self):
		current_date = datetime.now(tz=timezone("America/New_York"))

		return any(
				model_settings.request_per_day_used < model_settings.request_per_day_limit or current_date.day != model_settings.start_day.day for model_settings in self.models_settings
		)
	#
	#
	#
	#
	def get_lowest_useful_model_index(self):
		if self.check_models_limits():
			current_date = datetime.now(tz=timezone("America/New_York"))
			index = 0

			for i in range(len(self.models_settings)):
				if self.models_settings[i].request_per_day_used < self.models_settings[i].request_per_day_limit or current_date.day != self.models_settings[i].start_day.day:
					break
				else:
					index += 1

			return index
		else:
			raise GeminiNoUsefulModelsException()
	#
	#
	#
	#
	def use_next_model(self):
		if self.check_models_limits():
			self.current_model_index = (self.current_model_index + 1) % len(self.models_settings)
			self.current_model = Gemini(self.models_settings[self.current_model_index])

			return self.current_model
		else:
			raise GeminiNoUsefulModelsException()
	#
	#
	#
	#
	def get_model_index(self, model_api_key: str = None):
		if model_api_key:
			for i in range(len(self.models_settings)):
				if self.models_settings[i].api_key == model_api_key:
					return i

		raise AttributeError("This API key doesn't found")
	#
	#
	#
	#
	def use_model(self, model_index: int = None, model_api_key: str = None):
		if model_index and model_api_key:
			raise AttributeError("You can't use both model_index and model_api_key")
		elif not model_index and not model_api_key:
			raise AttributeError("You must provide model_index or model_api_key")

		if self.check_models_limits():
			self.current_model_index = model_index if model_index else self.get_model_index(model_api_key)
			self.current_model = Gemini(self.models_settings[self.current_model_index])

			return self.current_model
		else:
			raise GeminiNoUsefulModelsException()
	#
	#
	#
	#
	def use_current_model(self):
		return self.current_model
	#
	#
	#
	#
	def reset_models_settings(self, gemini_settings: list[GeminiSettings]):
		self.models_settings = gemini_settings
		self.current_model_index = self.get_lowest_useful_model_index()
