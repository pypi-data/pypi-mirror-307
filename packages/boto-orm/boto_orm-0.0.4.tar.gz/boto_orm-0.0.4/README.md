# dynamodb_manager
Фреймворк для управления сервисами YandexCloud в serverless режиме на основе библиотеки `botocore` и `pydantic`.
С помощью фреймворка можно создавать объекты таблицы базы данных dynamodb и стандартного хранилища s3. И управлять непосредственно ими с помощью оптимизированного интерфейса. Названия методов идентичны методам библиотеки `botocore`, поэтому работать с этим фреймворком опытным программистам будет не сложно. Поскольку во фреймворке реализована далеко не вся функциональность библиотеки `botocore`, то в методах классов оставлены аргументы `**kwargs`, где вы можете использовать более тонкие запросы к AWS-сервисам YandexCloud. Проект находится в пилотном режиме, поэтому, если есть какие предложения по совершенствованию проекта, буду рад сотрудничеству.

## Работа с базой данных dynamodb

Для создания таблицы нужно определить ключевую схему с помощью класса `KeySchema`. Импортируем и объявим его экземпляр.

```python
from boto_orm.models.db_model import KeySchema

key_schema = KeySchema(HASH='name', RANGE='user_id')

```
Также определим схему таблицы с помощью класса на базе модели `DBModel`. Имена ключей, объявленные в ключевой схеме, должны присутствовать в классе модели.

```python
from boto_orm.models.db_model import DBModel

class Table(DBModel):
    name: str
    user_id: int
    create: float

```
Для ограничения пропускной способности, воспользуйтесь экземпляром класса `ProvisionedThroughput`.

```python
from boto_orm.db_manager import ProvisionedThroughput
prov = ProvisionedThroughput(ReadCapacityUnits=1, WriteCapacityUnits=1)
```

Для работы с сервисами AWS необходимо использование переменных окружения. Для этого создадим файл `boto-orm.yaml` в корневом каталоге со следующим содержимым (example заменить на свои переменные):
```yaml
session:
    access_key: 'key example'
    secret_key: 'secret example'
db_config:
    service_name: 'dynamodb'
    endpoint_url: 'https://example.com'
    region_name: 'ru-central1'
s3_config:
    service_name: 's3'
    endpoint_url: 'https://storage.example.com'
    region_name: 'ru-central1'
```

Либо создать свой конфиг на базе экземпляров классов `AWSConfig` и `AWSSession`.

```python
from boto_orm.models.config import AWSConfig, AWSSession

session = AWSSession(access_key: str = 'example', secret_key: str = 'example')
config = AWSConfig(service_name: str = 'example', endpoint_url: str = 'example', region_name: str = 'example')
```

Можно создать свой файл конфигурации `.yaml`, для этого необходимо сделать свой наследный класс от `boto_orm.models.config.BaseConfig`.
```py
class Configure(BaseConfig):
    session: AWSSession
    db_config: AWSConfig
    s3_config: AWSConfig

    model_config = SettingsConfigDict(yaml_file='.yaml')
```
Создать таблицу можно с помощью метода `create_table` экземпляра класса `DynamodbManage`

```python
from boto_orm.db_manager import DynamodbManage

db = DynamodbManage(table_name='Table_test')
db.create_table(key_schema, attribute=Table, provisioned_throughput=prov)
```
Экземпляр класса `DynamodbManage` имеет следующие аргументы:
```python
resource_name: str # название таблицы
config: Union[AWSConfig, dict] # конфигурация ресурсного клиента:
    service_name: Any['dynamodb', 's3'],
    endpoint_url: str
    region_name: str
session_aws: Union[AWSSession, dict] # конфигурация сессии botocore:
    access_key: str
    secret_key: str
```

Добавить элемент в таблицу можно с помощью команды:
```python
from boto_orm.models.db_model import DBModel

class Table(DBModel):
    name: str
    user_id: int
    create: float

data = Table(name='Name', user_id=238, create=19.97)
db = DynamodbManage(table_name='Table_test')
db.put_item(data)
```
Запрос по параметрам значений ключей
```python
response = db.query(Key('name').eq(value=['Tso']), range=Key('user_id').eq([239]))
```
Для запроса возможно использование значения только ключа партицирования. Также во фреймворке предусмотрена возможность фильтрации по параметрам, не являющимися ключами:
```python
from boto_orm.filter import Key, Filter

response = db.query(Key('name').eq(value=['Tso']), filters=Filter('user_id').ge(249))
```
Для фильтрации используется экземпляр класса `Filter`, где в качестве параметра используется имя столбца, а значение аргумента вводится в методе.
Для класса `Key` и `Filter` актуальны следующие методы:
* eq - Операция эквивалентности
* ne - Операция отрицания
* begins_with - Операция поиска строки, начинайщийся с value
* le - Операция меньше или равно
* lt - Операция меньше
* ge - Операция больше или равно
* gt - Операция больше
* between - Операция между.
Для операции сканирования базы данных используется метод `scan`.
```python
response = db.scan(filters=Filter('user_id').ge(237))
```
Метод может принимать следующие необязательные аргументы:
* need_args: Optional[List[str]] = None - запрос требуемых аргументов
* filters: Optional[Filter] = None - экземпляр класса Filter, используется для фильтрации значений столбцов в таблице.
Примеры использования низкоуровневых фильтров.
* [Dynamodb scan() using FilterExpression](https://www.iditect.com/faq/python/dynamodb-scan-using-filterexpression.html)
* [Boto3 DynamoDB Tutorial](https://hands-on.cloud/boto3/dynamodb/)
* [Официальная документация](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html)


## Работа с хранилищем s3
Создаём экземпляр клиента `S3Manager` для работы с бакетом
```python
from boto_orm.s3_manager import S3Manager

s3 = S3Manager(bucket_name='serverless-shortener')
```
Для создания бакета можно воспользоваться метода `create_bucket`.
```python
response = s3.create_bucket()
```
Загрузить строку или байты в бакет можно с помощью метода `put_object`.
```py
response = s3.put_object('TEST', name_file='test.txt')
```
Загрузить файл можно указав путь файла в методе `upload_file`:
```py
response = s3.upload_file(file_path='file/test.py', name_file='test.py')
```
Удалить один или несколько объектов можно следующим образом:
```py
response = s3.delete_objects(['manager.py', 'test.txt'])
```
Загрузить список объектов бакета можно с помощью метода `list_objects`
```py
response = s3.list_objects()
```
Загрузить объект файла можно с помощью метода `get_object`
```py
response = s3.get_str_object('index.html')
print(response['Body'].read())
```
В качестве альтернативы можно воспользоваться методом строкового представления загружаемого файла `get_str_object`. Дополнительным параметром можно добавить кодировку.
```py
response = s3.get_str_object('index.html', encoding='utf-8')
```
