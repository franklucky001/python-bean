# -*- coding:utf-8 -*-
from typing import Callable, Any
from bean.fields.bean_field import BeanField
from bean.bean_error import BeanValueError, BeanAssertError
from bean.type_utils import is_int, is_float


class IntField(BeanField):

    def __init__(self,
                 required: bool = False,
                 minimum: int = None,
                 maximum: int = None,
                 default: int = None,
                 parse_handler: Callable[[Any], int] = None):
        self.minimum = minimum
        self.maximum = maximum
        self.default = default
        handler = parse_handler or self.parse_int
        super(IntField, self).__init__(required=required, parse_handler=handler)

    @property
    def value(self) -> int:
        return self._bean_value

    @value.setter
    def value(self, value):
        if not self.required and value is None:
            if self.default:
                self._bean_value = self.default
                return
            else:
                raise BeanValueError("int default value unset when bind from None", exception_path=("value", "default"))
        if isinstance(value, int):
            self._bean_value = value
        else:
            self._bean_value = self.parse_handler(value)
        self.check_min_max()

    def check_min_max(self):
        value = self._bean_value
        if self.minimum:
            try:
                assert value >= self.minimum
            except AssertionError:
                msg = f"{value} is less than minimum {self.minimum}"
                exp = BeanAssertError(msg, exception_path=("int", "minimum"))
                raise exp
        if self.maximum:
            try:
                assert value <= self.maximum
            except AssertionError:
                msg = f"{value} is greater than maximum {self.maximum}"
                exp = BeanAssertError(msg, exception_path=("int", "maximum"))
                raise exp

    @staticmethod
    def parse_int(value) -> int:

        if isinstance(value, str):
            if is_int(value):
                return int(value)
            elif is_float(value):
                return int(float(value))
            else:
                msg = f'expect value numeric str, found {value}'
                raise BeanValueError(message=msg, exception_path=("int.parse",))
        elif isinstance(value, float):
            return int(value)
        else:
            msg = f'expect value of int or numeric str, found {type(value)}'
            raise BeanValueError(message=msg, exception_path=("int.parse",))
