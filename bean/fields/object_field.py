# -*- coding:utf-8 -*-
import json
import copy
from typing import List, Dict, Callable, Any, TypeVar
from bean.fields.bean_field import BeanField
from bean.model.bean_model import BeanModel
from bean.bean_error import BeanValueError, BeanAssertError, BeanValidationError

PropertiesType = TypeVar("PropertiesType", Dict[str, BeanField], BeanModel)


class ObjectField(BeanField):

    def __init__(self,
                 required: bool = False,
                 properties: PropertiesType = None,
                 required_fields: List[str] = None,
                 parse_handler: Callable[[Any], Dict] = None):
        self.required_fields = required_fields
        self._bean_properties: PropertiesType = properties
        handler = parse_handler or self.parse_object
        super(ObjectField, self).__init__(required, handler)

    def __getitem__(self, item):
        return self._bean_value.__getitem__(item)

    @property
    def value(self) -> Dict[str, Any]:
        properties = dict()
        for k, item in self._bean_value.items():
            properties[k] = item.value
        return properties

    @value.setter
    def value(self, value):
        if self._bean_properties is None:
            self._bean_value = {}
            return
        if isinstance(value, dict):
            value_decode = value
        else:
            value_decode = self.parse_handler(value)
        if not isinstance(self._bean_properties, BeanModel):
            object_value = dict()
            for k, field in self._bean_properties.items():
                val = value_decode.get(k, None)
                if not val:
                    continue
                field.value = val
                object_value[k] = field
            self._bean_value = object_value
        else:
            self._bean_properties.bind(value_decode)
            self._bean_value = copy.deepcopy(self._bean_properties.model_value)

    @staticmethod
    def parse_object(value):
        if isinstance(value, str):
            value_decode = json.loads(value)
            return value_decode
        else:
            msg = f'expect value type dict or dict of json array, found {type(value)}'
            raise BeanValueError(msg, exception_path=("object.parse",))
