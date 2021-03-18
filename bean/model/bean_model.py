# -*- coding:utf-8 -*-
import copy
from typing import Dict, Any
from bean.model.model_meta import ModelMeta
from bean.bean_error import BeanValueError, BeanAssertError, BeanValidationError


class BeanModel(dict, metaclass=ModelMeta):

    def __init__(self, **kwargs):
        reflect_mappings = getattr(self, "__reflect_mapping__", {})
        super(BeanModel, self).__init__(**kwargs)
        field_mappings = getattr(self, "__field_mapping__")
        self.mappings = copy.deepcopy(field_mappings) or copy.deepcopy(reflect_mappings)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"{self.__class__.__name__} object has no attribute : {item}")

    def __setattr__(self, key, value):
        self[key] = value

    @property
    def value(self):
        data_dic = dict()
        for k, field in self.mappings.items():
            data_dic[k] = field.value
        return data_dic

    @property
    def model_value(self):
        bean_dic = dict()
        for k, field in self.mappings.items():
            bean_dic[k] = field
        return bean_dic

    @staticmethod
    def check_required(k, field, value):
        from bean.fields import BeanField
        if isinstance(field, BeanField) and field.required:
            try:
                assert value is not None
            except AssertionError:
                msg = f"{k} is required property"
                raise BeanAssertError(msg, exception_path=("property", k))

    def bind(self, data: Dict[str, Any]) -> None:
        for k, field in self.mappings.items():
            value = data.get(k, None)
            self.check_required(k, field, value)
            try:
                field.value = value
                setattr(self, k, field)
            except BeanValidationError as e:
                context = tuple(e.context) + (e, )
                context = copy.deepcopy(context)
                parent_path = tuple(e.exception_path)
                parent = BeanValueError(e.message, exception_path=parent_path, parent=copy.deepcopy(e.parent))
                exp = BeanValidationError(e.message, exception_path=("property", k), context=context, parent=parent)
                raise exp

    def __repr__(self):
        name = getattr(self, "__field_name__")
        values = ','.join([f"{k}:{field.value}" for k, field in self.mappings.items()])
        return f"class Object {name}, ({values})"

    def __str__(self):
        values = ','.join([f"{k}={field.value}" for k, field in self.mappings.items()])
        address = id(self)
        return f"{self.__class__.__name__} object in {address} ({values})"
