# -*- coding:utf-8 -*-
import json
import copy
from typing import List, Callable, Any, TypeVar
from bean.fields.bean_field import BeanField
from bean.model.bean_model import BeanModel
from bean.bean_error import BeanValueError, BeanAssertError
ItemType = TypeVar('ItemType', BeanField, BeanModel)


class ArrayField(BeanField):

    def __init__(self,
                 required: bool = False,
                 items: List[ItemType] = None,
                 array_item: ItemType = None,
                 min_length: int = None,
                 max_length: int = None,
                 parse_handler: Callable[[Any], List] = None):
        self.min_length = min_length
        self.max_length = max_length
        handler = parse_handler or self.parse_array
        self._bean_items: List[ItemType] = items
        self._bean_array_item: ItemType = array_item
        super(ArrayField, self).__init__(required, handler)

    def __len__(self):
        return self._bean_value.__len__()

    def __getitem__(self, item):
        return self._bean_value[item]

    @property
    def value(self) -> list:
        if self._bean_value is None:
            return []
        values = []
        for item in self._bean_value:
            if isinstance(item, BeanField):
                values.append(item.value)
            else:
                decode_value = {k: field.value for k, field in item.model_value.items()}
                values.append(decode_value)
        return values

    @value.setter
    def value(self, value):
        if self._bean_items is None and self._bean_array_item is None:
            self._bean_value = []
            return
        if isinstance(value, list):
            value_decode = value
        else:
            value_decode = self.parse_handler(value)
        list_value = []
        if self._bean_items:
            for (item_value, bean_item) in zip(value_decode, self._bean_items):
                if isinstance(bean_item, BeanField):
                    bean_item.value = item_value
                else:
                    bean_item.bind(item_value)
                list_value.append(bean_item)
        else:
            for item_value in value_decode:
                bean_item = copy.deepcopy(self._bean_array_item)
                if isinstance(bean_item, BeanField):
                    bean_item.value = item_value
                else:
                    bean_item.bind(item_value)
                list_value.append(bean_item)
        self._bean_value = list_value
        self.check_length()

    def check_length(self):
        array = self._bean_value
        if self.min_length:
            try:
                assert len(array) >= self.min_length
            except AssertionError:
                msg = f"{len(array)} is less than min length {self.min_length} of array"
                exp = BeanAssertError(msg, exception_path=("length", "minimum"))
                raise exp
        if self.max_length:
            try:
                assert len(array) <= self.max_length
            except AssertionError:
                msg = f"{len(array)} is greater than max length {self.max_length} of array"
                exp = BeanAssertError(msg, exception_path=("length", "maximum"))
                raise exp

    @staticmethod
    def parse_array(value):
        if isinstance(value, str):
            value_decode = json.loads(value)
            return value_decode
        else:
            msg = f'expect value of list or list of json array, found {type(value)}'
            raise BeanValueError(message=msg, exception_path=("array.parse", ))

