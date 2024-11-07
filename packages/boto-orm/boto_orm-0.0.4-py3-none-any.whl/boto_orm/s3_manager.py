from typing import Union, List
from boto_orm.models.client import Client
from boto_orm.models.config import AWSConfig, AWSSession, config


class S3Manager(Client):
    def __init__(self, bucket_name: str,
                 config: Union[AWSConfig, dict] = config.s3_config,
                 session_aws: Union[AWSSession, dict] = config.session):
        super().__init__(bucket_name, config, session_aws)

    def create_bucket(self, **kwargs):
        data = {'Bucket': self.resource_name}
        if kwargs:
            data.update(kwargs)
        return self.client.create_bucket(**data)

    def put_object(self, body: Union[bytes, str], name_file: str, storage_class: str = 'STANDARD', **kwargs):
        data = {
            'Bucket': self.resource_name,
            'Body': body,
            'Key': name_file,
            'StorageClass': storage_class
            }
        if kwargs:
            data.update(kwargs)
        return self.client.put_object(**data)

    def upload_file(self, file_path: str, name_file: str, storage_class: str = 'STANDARD', **kwargs):
        with open(file_path, 'rb') as file:
            data = {
                'Bucket': self.resource_name,
                'Body': file,
                'Key': name_file,
                'StorageClass': storage_class
                }
            if kwargs:
                data.update(kwargs)
            return self.client.put_object(**data)

    def delete_objects(self, objects: List[str], **kwargs):
        data = {
            'Bucket': self.resource_name,
            'Delete': {
                'Objects': [
                    {'Key': item}
                        for item in objects],
            'Quiet': False
            },
        }
        if kwargs:
            data.update(kwargs)
        return self.client.delete_objects(**data)

    def list_objects(self, **kwargs):
        data = {'Bucket': self.resource_name}
        if kwargs:
            data.update(kwargs)
        return self.client.list_objects_v2(**data)

    def get_object(self, file_name: str, **kwargs):
        data = {
            'Bucket': self.resource_name,
            'Key': file_name
            }
        if kwargs:
            data.update(kwargs)
        return self.client.get_object(**data)

    def get_str_object(self, file_name: str, encoding='utf-8', **kwargs):
        data_bytes = self.get_object(file_name, **kwargs)['Body'].read()
        return str(data_bytes, encoding=encoding)
