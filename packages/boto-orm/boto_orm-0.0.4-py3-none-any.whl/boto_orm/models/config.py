from pydantic import BaseModel
from pydantic_settings import (BaseSettings, SettingsConfigDict,
                               PydanticBaseSettingsSource, YamlConfigSettingsSource)
from typing import Type, Tuple
import os.path

class AWSSession(BaseModel):
    access_key: str
    secret_key: str

class AWSConfig(BaseModel):
    service_name: str
    endpoint_url: str
    region_name: str

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(yaml_file='boto-orm.yaml')

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls), )


class Configure(BaseConfig):
    session: AWSSession
    db_config: AWSConfig
    s3_config: AWSConfig


if os.path.exists('boto-orm.yaml'):
    config = Configure()
else:
    config = None
