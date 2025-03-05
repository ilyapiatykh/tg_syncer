import yaml
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

CONFIG_PATH = "configs/prod.yaml"


class Config(BaseSettings):
    api_id: SecretStr = Field(validation_alias="API_ID")
    api_hash: SecretStr = Field(validation_alias="API_HASH")

    target_channel_id: int
    source_channels_ids: list[int]

    @classmethod
    def from_file(cls):
        with open(CONFIG_PATH, "r") as f:
            content = yaml.full_load(f)

        return cls.model_validate(content)
