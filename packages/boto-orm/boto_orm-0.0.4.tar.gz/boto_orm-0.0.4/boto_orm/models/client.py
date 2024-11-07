import botocore
import botocore.session
from botocore.session import Session
from typing import Union

from boto_orm.models.db_model import DBModel
from boto_orm.models.config import AWSConfig, AWSSession


class Client:
    """Родительский класс для инициализации клиента для управления AWS-service. Оптимизирован для работы в YandexCloud.
        :param resource_name: str - название таблицы или бакета
        :param config: Union[AWSConfig, dict] - конфигурация ресурсного клиента: service_name: Annotated[str, 'dynamodb', 's3'], region_name: str, endpoint_url: str
        :param session_aws: Union[AWSSession, dict] - конфигурация сессии botocore: access_key: str, secret_key: str
    """
    def __init__(self, resource_name: str,
                 config: Union[AWSConfig, dict],
                 session_aws: Union[AWSSession, dict]):
        config = self._check_type_models(config, AWSConfig)
        session_aws = self._check_type_models(session_aws, AWSSession)
        _aws: Session = botocore.session.get_session()
        _aws.set_credentials(**session_aws)
        self.resource_name = resource_name
        self.client = _aws.create_client(**config)

    @staticmethod
    def _check_type_models(arg: Union[dict, DBModel], dataclass_name: type = None):
        if dataclass_name and isinstance(arg, dataclass_name):
            return arg.__dict__
        if isinstance(arg, DBModel):
            return arg.model_dump()
        if isinstance(arg, dict):
            return arg