# -*- coding:utf-8 -*-


class BeanField:

    def __init__(self, required: bool = False, parse_handler=None):
        self.required = required
        self.parse_handler = parse_handler
        self._bean_value = None

    @property
    def value(self):
        return self._bean_value

    @value.setter
    def value(self, value):
        self._bean_value = value
