from pydantic import BaseModel
from dataclasses import dataclass
from typing import Optional, Any, Dict, Union

PARAMS = {
            int: 'N',
            float: 'N',
            str: 'S',
            bool: 'BOOL',
            None: 'NULL',
            list: 'L',
            tuple: 'L',
            dict: 'M',
            bytes: 'B'
        }

PARAMS_REVERSE = {
    'N': lambda x: float(x) if '.' in x else int(x),
    'S': str,
    'BOOL': bool,
    'NULL': None,
    'L': list,
    'M': dict,
    'B': bytes
}

def _params_convert(arg: type, value: Any = None):
    def convert(arg: type):
        if arg not in PARAMS:
            return PARAMS[str]
        return PARAMS[arg]

    def recursion(value):
        result = {}
        condition = lambda x: type(x) not in [str, int, float, bytes]
        if isinstance(value, dict):
            for key, val in value.items():
                if isinstance(val, dict):
                    result[key] = recursion(val)
                else:
                    result[key] = {convert(type(val)): val if condition(val) else str(val)}
            return {'M': result}
        elif isinstance(value, list):
            return {'L': [recursion(item) for item in value]}
        return {convert(type(value)): value if condition(value) else str(value)}

    if value:
        return recursion(value)
    return convert(arg)

def _dump_dict(data: Dict[str, Dict[str, str]]):
    result = {}
    for key, values in data.items():
        if isinstance(values, dict):
            types, value = tuple(values.items())[0]
            if types == 'M':
                result[key] = _dump_dict(value)
            elif types == 'L':
                result[key] = [_dump_dict(item) for item in value]
            elif types not in PARAMS_REVERSE.keys():
                return {types: _dump_dict(value)}
            else:
                result[key] = PARAMS_REVERSE[types](value)
        else:
            return values

    return result

class DBModel(BaseModel):
    def dump_dynamodb(self):
        return {key: _params_convert(self.__annotations__[key], value)
                for key, value in self.model_dump().items()}

    @classmethod
    def dump_schema_db(cls):
        return {key: _params_convert(value) for key, value in
                            cls.__annotations__.items()}


@dataclass
class KeySchema:
    HASH: str
    RANGE: Optional[str] = None

    def __call__(self, HASH_VALUE: Union[str, int, None] = None, RANGE_VALUE: Union[str, int, None] = None):
        """Функция для запроса get_item по значениям HASH и RANGE.
        """
        data = {}
        if RANGE_VALUE:
            data[self.RANGE] = RANGE_VALUE
        if HASH_VALUE:
            data[self.HASH] = HASH_VALUE
        if data:
            return data
        assert KeyError('Not arguments to query')
