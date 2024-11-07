from dataclasses import dataclass
from typing import Dict, Optional, Union, List, Any
from boto_orm.models.client import Client
from boto_orm.models.config import AWSConfig, AWSSession, config
from boto_orm.models.db_model import KeySchema, DBModel, _params_convert, _dump_dict
from boto_orm.filter import Key, Filter

@dataclass
class ProvisionedThroughput:
    """Обеспеченная пропускная способность
        Представляет заданные параметры пропускной способности для указанной таблицы или индекса.
        Параметры можно изменить с помощью UpdateTable операции.
    """
    ReadCapacityUnits: int
    WriteCapacityUnits: int

class DynamodbManage(Client):
    """Дочерний класс управления таблицами DynamoDB в облачных сервисах YandexCloud.
    """
    def __init__(self, table_name: str, config: Union[AWSConfig, dict] = config.db_config,
                 session_aws: Union[AWSSession, dict] = config.session):
        super().__init__(table_name, config, session_aws)

    @staticmethod
    def _table_params(resource_name: str, key_schema: Dict[str, str], attribute: Dict[str, str],
                      provisioned_throughput: Optional[Dict[str, str]] = None):
        table_creation_params = {
            'TableName': resource_name,
            'KeySchema': [
                {
                    'AttributeName': value,
                    'KeyType': key
                }
                for key, value in key_schema.items() if value
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': key,
                    'AttributeType': value
                }
                for key, value in attribute.items()
            ]
        }
        if provisioned_throughput:
            table_creation_params["ProvisionedThroughput"] = provisioned_throughput

        return table_creation_params


    @staticmethod
    def _check_arg_models(arg: Union[DBModel, Dict[str, dict]]):
        if isinstance(arg, DBModel):
            return arg.dump_dynamodb()
        elif isinstance(arg, dict):
            return {key: _params_convert(type(value), value)
                for key, value in arg.items()}
        else:
            assert TypeError('Uncorrect type param "arg"')


    @staticmethod
    def _check_param_models(attribute: Union[Dict[str, str], DBModel], key_schema: Union[Dict[str, str], KeySchema]):
        if isinstance(key_schema, KeySchema):
            key_schema = {key: value for key, value in key_schema.__dict__.items() if value}
        if issubclass(attribute, DBModel):
            attribute = dict(filter(lambda item: item[0] in key_schema.values(),
                                    attribute.dump_schema_db().items()))
        return key_schema, attribute

    @staticmethod
    def _error_handler(response: dict):
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Item' in response.keys():
                response['Item'] = _dump_dict(response['Item'])
            elif 'Items' in response:
                response['Items'] = [_dump_dict(item) for item in response['Items']]
            return response
        else:
            assert ConnectionError(response['ResponseMetadata'])


    def create_table(self, key_schema: Union[Dict[str, str], KeySchema],
                      attribute: Union[Dict[str, str], DBModel],
                      provisioned_throughput: Union[Dict[str, str], ProvisionedThroughput, None] = None):
        """Метод создания таблицы.
            :type key_schema: Union[Dict[str, str], KeySchema]
            :param key_schema: Рекомендуется использование dataclass для установки ключей партицирования
                                'HASH' и сортировки 'RANGE'
            :type attribute: Union[Dict[str, str], DBModel]
            :param attribute: Рекомендуется использование модели на базе DBModel с аргументами arg: type = 'value'
            :type provisioned_throughput: Union[Dict[str, str], ProvisionedThroughput, None] = None)
            :param provisioned_throughput: Предусмотренные параметры пропускной способности для глобального
                                        вторичного индекса, состоящие из единиц пропускной способности чтения и записи.
        """
        key_schema, attribute = self._check_param_models(attribute, key_schema)
        if provisioned_throughput:
            provisioned_throughput = self._check_type_models(provisioned_throughput, ProvisionedThroughput)
        table_creation_params = self._table_params(self.resource_name, key_schema, attribute, provisioned_throughput)
        response = self.client.create_table(**table_creation_params)
        return self._error_handler(response)


    def put_item(self, data: DBModel):
        """Метод добавления данных в таблицу. Автоматически определяет тип и значение переменных
            из экземпляра класса DBModel
            :type data: DBModel
            :param data: принимает в качестве аргумента экземпляр dataclass
        """
        data = self._check_arg_models(data)
        response = self.client.put_item(TableName=self.resource_name, Item=data)
        return self._error_handler(response)

    def get_item(self, keys: KeySchema, need_args: Optional[List[str]] = None, **kwargs):
        """Метод запроса значения из таблицы по значению ключа / ключей.
            :type need_args: Optional[List[str]] = None
            :param need_args: список требуемых параметров для вызова
            :type keys: Dict[str, str | int ] или экземпляр датакласса KeySchema keys(HASH_VALUE, RANGE_VALUE)
            :param keys: ключи доступа в формате {'key': 'value'}
        """
        data = {
            'TableName': self.resource_name,
            'Key': self._check_arg_models(keys)
        }
        if need_args:
            data['ProjectionExpression'] = ', '.join(need_args)
        if kwargs:
            data.update(kwargs)
        return self._error_handler(self.client.get_item(**data))

    def delete_item(self, keys: KeySchema):
        """Метод удаления значения из таблицы по значению ключа / ключей.
            :type keys: Dict[str, str | int ] или экземпляр датакласса KeySchema keys(HASH_VALUE, RANGE_VALUE)
            :param keys: {'key': 'value'}
        """
        keys = self._check_arg_models(keys)
        return self.client.delete_item(TableName=self.resource_name, Key=keys)

    def scan(self, need_args: Optional[List[str]] = None, filters: Optional[Filter] = None, **kwargs):
        """Метод сканирования базы данных. Для сортировки может быть использован класс Filter.
            :type need_args: Optional[List[str]] = None
            :param need_args: запрос требуемых аргументов
            :type filters: Optional[Filter] = None
            :param filters: экземпляр класса Filter, используется для фильтрации значений столбцов в таблице.
        """
        data = {'TableName': self.resource_name}
        if need_args:
            data['ProjectionExpression'] = ', '.join(need_args)
        if filters:
            data.update(filters)
        if kwargs:
            data.update(kwargs)
        return self._error_handler(self.client.scan(**data))

    def query(self, hash: Key, range: Optional[Key] = None,
              need_args: Optional[List[str]] = None, filters: Optional[Filter] = None, **kwargs):
        """Метод запроса к базе данных по данным ключей. Для сортировки может быть использован класс Key.
            :type hash: Key
            :param hash: ключ партицирования
            :type range: Optional[Key] = None
            :param range: ключ сортировки
            :type need_args: Optional[List[str]] = None
            :param need_args: запрос требуемых аргументов
            :type filters: Optional[Filter] = None
            :param filters: экземпляр класса Filter, используется для фильтрации значений столбцов в таблице.
        """
        data = {'TableName': self.resource_name}
        if range:
            hash.update(range)
        data['KeyConditions'] = hash
        if need_args:
            data['ProjectionExpression'] = ', '.join(need_args)
        if filters:
            data.update(filters)
        if kwargs:
            data.update(kwargs)
        return self._error_handler(self.client.query(**data))

    def update_item(self, keys: KeySchema, args: Dict[str, Any], **kwargs):
        """Метод обновления значений из таблицы по значению ключа / ключей.
            :type args: Dict[str, Any]
            :param args: словарь по схеме атрибут: значение для обновления атрибутов таблицы по значению ключа.
                обновление значения словаря по схеме 'atr1.atr2'
            :type keys: Dict[str, str | int ] или экземпляр датакласса KeySchema keys(HASH_VALUE, RANGE_VALUE)
            :param keys: ключи доступа в формате {'key': 'value'}
        """
        data = {
            'TableName': self.resource_name,
            'Key': self._check_arg_models(keys),
            'ReturnValues': "UPDATED_NEW"

        }
        attribute = [f'{item} = :arg_{i}' for i, item in enumerate(args.keys())]
        data['UpdateExpression'] = f"set {', '.join(attribute)}"
        data['ExpressionAttributeValues'] = {
            f':arg_{i}': _params_convert(type(value), value)
            for i, value in enumerate(args.values())
        }
        if kwargs:
            data.update(kwargs)
        return self._error_handler(self.client.update_item(**data))

    def delete_table(self):
        """Метод удаления таблицы из базы данных. Название таблицы берётся из resource_name экземпляра класса
        """
        return self.client.delete_table(TableName=self.resource_name)