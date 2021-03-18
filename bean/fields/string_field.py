# -*- coding:utf-8 -*-
import re
from typing import Callable, Any
from bean.fields.bean_field import BeanField
from bean.bean_error import BeanValueError, BeanAssertError


class StringField(BeanField):

    def __init__(self,
                 required: bool = False,
                 min_length: int = None,
                 max_length: int = None,
                 default: str = None,
                 pattern: str = None,
                 parse_handler: Callable[[Any], str] = None):
        self.min_length = min_length
        self.max_length = max_length
        self.default = default
        self.pattern = pattern
        handler = parse_handler or self.parse_string
        super(StringField, self).__init__(required, handler)

    @property
    def value(self) -> str:
        return self._bean_value

    @value.setter
    def value(self, value):
        if not self.required and value is None:
            if self.default:
                self._bean_value = self.default
                return
            else:
                raise BeanValueError("string default value unset when bind from None", exception_path=("value", "default"))
        if isinstance(value, str):
            self._bean_value = value
        else:
            self._bean_value = self.parse_handler(value)
        self.check_value()

    def check_value(self):
        if self.pattern:
            self.check_pattern()
        else:
            self.check_length()

    def check_length(self):
        value = self._bean_value
        if self.min_length:
            try:
                assert len(value) >= self.min_length
            except AssertionError:
                msg = f"{len(value)} is less than minimum length {self.min_length}"
                raise BeanAssertError(msg, exception_path=("string.length.min",))
        if self.max_length:
            try:
                assert len(value) < self.max_length
            except AssertionError:
                msg = f"{len(value)} is greater than minimum length {self.max_length}"
                raise BeanAssertError(msg, exception_path=("string.length.max",))

    def check_pattern(self):
        value = self._bean_value
        try:
            r = re.compile(pattern=self.pattern)
            m = r.search(value)
            if not m:
                msg = f"{value} does not match {self.pattern}"
                raise BeanValueError(msg, exception_path=("string.pattern",))
        except ValueError:
            msg = f'string pattern {self.pattern} is invalid'
            raise BeanAssertError(message=msg, exception_path=("string.pattern",))

    @staticmethod
    def parse_string(value) -> str:
        if isinstance(value, int) or isinstance(value) or isinstance(bool):
            return str(value)
        else:
            msg = f'expect value string or int|float|bool ), found {type(value)}'
            raise BeanValueError(message=msg, exception_path=("string.parse",))
