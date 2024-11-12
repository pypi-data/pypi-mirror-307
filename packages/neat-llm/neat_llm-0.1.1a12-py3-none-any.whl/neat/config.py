import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from loguru import logger
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from neat.constants import LLMModel

STRUCTURED_OUTPUT_MODELS = ["gpt-4o-mini", "gpt-4o-2024-08-06"]
UNSUPPORTED_RESPONSE_MODELS = ["command-r", "command-r-plus"]
UNSUPPORTED_TOOL_MODELS = []

current_dir = Path(__file__).parent
env_file_path = current_dir.parent / ".env"


class Settings(BaseSettings):
    db_file: str = Field(default="prompt_versions.db", description="Database file path")
    default_model: LLMModel = Field(
        default=LLMModel.GPT_4O_MINI.model_name, description="Default LLM model"
    )
    default_temperature: float = Field(
        default=0.7, description="Default temperature for LLM"
    )
    log_level: str = Field(default="INFO", description="Logging level")

    # API Keys
    openai_api_key: Optional[SecretStr] = Field(default=None)
    anthropic_api_key: Optional[SecretStr] = Field(default=None)
    cohere_api_key: Optional[SecretStr] = Field(default=None)
    mistral_api_key: Optional[SecretStr] = Field(default=None)
    perplexityai_api_key: Optional[SecretStr] = Field(default=None)
    aws_access_key_id: Optional[SecretStr] = Field(default=None)
    aws_secret_access_key: Optional[SecretStr] = Field(default=None)
    aws_region_name: Optional[str] = Field(default=None)
    azure_api_key: Optional[SecretStr] = Field(default=None)
    azure_api_base: Optional[str] = Field(default=None)
    azure_api_version: Optional[str] = Field(default=None)
    azure_ad_token: Optional[SecretStr] = Field(default=None)
    azure_api_type: Optional[str] = Field(default=None)
    azure_ai_api_key: Optional[SecretStr] = Field(default=None)
    azure_ai_api_base: Optional[str] = Field(default=None)
    groq_api_key: Optional[SecretStr] = Field(default=None)
    fireworks_ai_api_key: Optional[SecretStr] = Field(default=None)
    togetherai_api_key: Optional[SecretStr] = Field(default=None)
    openrouter_api_key: Optional[SecretStr] = Field(default=None)
    or_site_url: Optional[str] = Field(default=None)
    or_app_name: Optional[str] = Field(default=None)

    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_file_encoding="utf-8",
        extra="allow",
    )


@lru_cache()
def get_settings(**kwargs) -> Settings:
    settings = Settings(**kwargs)
    return settings


settings: Settings = get_settings()


class Config:
    def __init__(self, settings: Settings = settings):
        self._settings = settings

    # Look for .env file in current directory and all parent directories
    current_dir = Path(__file__).resolve().parent
    env_file = None
    for parent in [current_dir] + list(current_dir.parents):
        if (parent / ".env").is_file():
            env_file = parent / ".env"
            break

    if env_file:
        load_dotenv(env_file)
    else:
        print("Warning: .env file not found")

    @property
    def openai_api_key(self):
        return settings.openai_api_key

    @openai_api_key.setter
    def openai_api_key(self, key: SecretStr):
        settings.openai_api_key = key
        os.environ["OPENAI_API_KEY"] = key.get_secret_value()

    @property
    def anthropic_api_key(self):
        return settings.anthropic_api_key

    @anthropic_api_key.setter
    def anthropic_api_key(self, key: SecretStr):
        settings.anthropic_api_key = key
        os.environ["ANTHROPIC_API_KEY"] = key.get_secret_value()

    @property
    def cohere_api_key(self):
        return settings.cohere_api_key

    @cohere_api_key.setter
    def cohere_api_key(self, key: SecretStr):
        settings.cohere_api_key = key
        os.environ["COHERE_API_KEY"] = key.get_secret_value()

    @property
    def mistral_api_key(self):
        return settings.mistral_api_key

    @mistral_api_key.setter
    def mistral_api_key(self, key: SecretStr):
        settings.mistral_api_key = key
        os.environ["MISTRAL_API_KEY"] = key.get_secret_value()

    @property
    def perplexityai_api_key(self):
        return settings.perplexityai_api_key

    @perplexityai_api_key.setter
    def perplexityai_api_key(self, key: SecretStr):
        settings.perplexityai_api_key = key
        os.environ["PERPLEXITYAI_API_KEY"] = key.get_secret_value()

    @property
    def groq_api_key(self):
        return settings.groq_api_key

    @groq_api_key.setter
    def groq_api_key(self, key: SecretStr):
        settings.groq_api_key = key
        os.environ["GROQ_API_KEY"] = key.get_secret_value()

    @property
    def fireworks_ai_api_key(self):
        return settings.fireworks_ai_api_key

    @fireworks_ai_api_key.setter
    def fireworks_ai_api_key(self, key: SecretStr):
        settings.fireworks_ai_api_key = key
        os.environ["FIREWORKS_AI_API_KEY"] = key.get_secret_value()

    @property
    def togetherai_api_key(self):
        return settings.togetherai_api_key

    @togetherai_api_key.setter
    def togetherai_api_key(self, key: SecretStr):
        settings.togetherai_api_key = key
        os.environ["TOGETHERAI_API_KEY"] = key.get_secret_value()

    def set_aws_credentials(
        self, access_key_id: SecretStr, secret_access_key: SecretStr, region_name: str
    ):
        settings.aws_access_key_id = access_key_id
        settings.aws_secret_access_key = secret_access_key
        settings.aws_region_name = region_name
        os.environ["AWS_ACCESS_KEY_ID"] = access_key_id.get_secret_value()
        os.environ["AWS_SECRET_ACCESS_KEY"] = secret_access_key.get_secret_value()
        os.environ["AWS_REGION_NAME"] = region_name

    def set_azure_credentials(
        self,
        api_key: SecretStr,
        api_base: str,
        api_version: str,
        ad_token: SecretStr = SecretStr(""),
        api_type: str = "",
    ):
        settings.azure_api_key = api_key
        settings.azure_api_base = api_base
        settings.azure_api_version = api_version
        settings.azure_ad_token = ad_token
        settings.azure_api_type = api_type
        os.environ["AZURE_API_KEY"] = api_key.get_secret_value()
        os.environ["AZURE_API_BASE"] = api_base
        os.environ["AZURE_API_VERSION"] = api_version
        if ad_token:
            os.environ["AZURE_AD_TOKEN"] = ad_token.get_secret_value()
        if api_type:
            os.environ["AZURE_API_TYPE"] = api_type

    def set_azure_ai_credentials(self, api_key: SecretStr, api_base: str):
        settings.azure_ai_api_key = api_key
        settings.azure_ai_api_base = api_base
        os.environ["AZURE_AI_API_KEY"] = api_key.get_secret_value()
        os.environ["AZURE_AI_API_BASE"] = api_base

    def set_openrouter_credentials(
        self, api_key: SecretStr, site_url: str = "", app_name: str = ""
    ):
        settings.openrouter_api_key = api_key
        settings.or_site_url = site_url
        settings.or_app_name = app_name
        os.environ["OPENROUTER_API_KEY"] = api_key.get_secret_value()
        if site_url:
            os.environ["OR_SITE_URL"] = site_url
        if app_name:
            os.environ["OR_APP_NAME"] = app_name


neat_config = Config()


def setup_logging(log_level: str):
    logger.remove()
    logger.add(
        sink=lambda msg: print(msg),
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )


setup_logging(settings.log_level)
