from boto_orm.models.db_model import _params_convert
from typing import Any

class Key:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def operator(key, value, operator):
        data = {'ComparisonOperator': operator}
        if value:
            data['AttributeValueList'] = [_params_convert(type(item), item)
                                            for item in value]
        return {key: data}

    def eq(self, value: list):
        """Операция эквивалентности
        """
        return self.operator(self.name, value, operator='EQ')

    def ne(self, value: list):
        """Операция отрицания
        """
        return self.operator(self.name, value, operator='NE')

    def begins_with(self, value: list):
        """Операция поиска строки, начинайщийся с value
        """
        return self.operator(self.name, value, operator='BEGINS_WITH')

    def le(self, value: list):
        """Операция меньше или равно
        """
        return self.operator(self.name, value, operator='LE')

    def lt(self, value: list):
        """Операция меньше
        """
        return self.operator(self.name, value, operator='LT')

    def ge(self, value: list):
        """Операция больше или равно
        """
        return self.operator(self.name, value, operator='GE')

    def gt(self, value: list):
        """Операция больше
        """
        return self.operator(self.name, value, operator='GT')

    def between(self, value: list):
        """Операция между
        """
        return self.operator(self.name, value, operator='BETWEEN')

class Filter(Key):
    def __init__(self, name: str) -> None:
        self.name = name

    @staticmethod
    def operator(name: str, value: Any, operator: str = 'EQ'):
        lst_operator = {
            'EQ': '=',
            'NE': 'not',
            'IN': 'in',
            'LE': '<=',
            'LT': '<',
            'GE': '>=',
            'GT': '>',
            'BETWEEN': 'BETWEEN',
            'BEGINS_WITH': 'BEGINS_WITH'
        }
        data =  {
            'FilterExpression' : f'{name} {lst_operator["EQ"]} :value' ,
            'ExpressionAttributeValues' : {':value' : _params_convert(type(value), value)}
                }

        return data
