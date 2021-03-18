# -*- coding:utf-8 -*-
import json
from typing import List, Dict
from bean.model.reflect_model import ReflectModel
from bean.fields import IntField, FloatField, StringField, ArrayField, ObjectField, BeanField


class BeanFactory:

    def __init__(self):
        pass

    def create(self, schema_file) -> ReflectModel:
        with open(schema_file) as f:
            schema = json.load(f)
        root_type = schema['type']
        assert root_type == 'object', "expect type object in schema root node"
        properties = self._create_properties(schema['properties'], schema['required'])
        mappings = {}
        for k, field in properties.items():
            mappings[k] = field
        return ReflectModel(mappings)

    def _make_item(self, item, is_required=True) -> BeanField:
        m_type = item['type']
        if m_type == 'string':
            min_length = item.get('minLength', None)
            max_length = item.get('maxLength', None)
            pattern = item.get('pattern', None)
            item_field = self._create_string(is_required, min_length, max_length, pattern)
        elif m_type == 'integer' or m_type == 'number':
            minimum = item.get('minimum', None)
            maximum = item.get('maximum', None)
            if isinstance(minimum, float) or isinstance(maximum, float):
                item_field = self._create_float(is_required, minimum, maximum)
            else:
                item_field = self._creat_int(is_required, minimum, maximum)
        elif m_type == 'array':
            m_item = item['items']
            item_field = self._create_array(is_required, m_item)
        else:
            m_required = item['required']
            properties = item['properties']
            item_field = self._create_object(is_required, properties, required=m_required)
        return item_field

    def _create_properties(self, s_properties: Dict[str, Dict], required: List):
        properties = {}
        for m_name, m_property in s_properties.items():
            m_required = m_name in required
            item_field = self._make_item(m_property, is_required=m_required)
            properties[m_name] = item_field
        return properties

    def _create_object(self, is_required: bool, s_properties: Dict[str, Dict], required: List):
        properties = self._create_properties(s_properties, required)
        return ObjectField(required=is_required, properties=properties)

    def _create_array(self, is_required: bool, item: Dict):
        item_field = self._make_item(item)
        return ArrayField(required=is_required, array_item=item_field)

    @staticmethod
    def _create_string(is_required: bool, min_length, max_length, pattern):
        return StringField(required=is_required,
                           min_length=min_length,
                           max_length=max_length,
                           pattern=pattern)

    @staticmethod
    def _creat_int(is_required: bool, minimum, maximum):
        return IntField(required=is_required,
                        minimum=minimum,
                        maximum=maximum)

    @staticmethod
    def _create_float(is_required: bool, minimum, maximum):
        return FloatField(required=is_required,
                          minimum=minimum,
                          maximum=maximum)
