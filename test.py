# -*- coding:utf-8 -*-
import os
import sys
from bean.factory import BeanFactory
from bean.model.reflect_model import ReflectModel
from bean.bean_error import BeanValueError, BeanAssertError


schema_folder = "./schemas"


def test_basic():
    schema_file = os.path.join(schema_folder, 'basic.schema.json')
    data = {
        "name": "mike",
        "age": 20,
        "sex": "male"
    }
    run(schema_file, data)


def test_list():
    schema_file = os.path.join(schema_folder, 'list.schema.json')
    data = {
            "values": ["aaa", "bbb"]
    }
    run(schema_file, data)


def test_dict():
    schema_file = os.path.join(schema_folder, 'dict.schema.json')
    data = {
        'data': {
            'name': 'mike',
            'age': 20,
            'sex': 'male'
        }
    }
    run(schema_file, data)


def run(schema_file, data):
    factory = BeanFactory()
    model: ReflectModel = factory.create(schema_file)
    try:
        model.bind(data)
    except (BeanValueError, BeanAssertError) as e:
        src = '.'.join(e.absolute_path)
        print(e.message, f"caused by {src}")
        sys.exit(-1)
    print(model)
    print(model.value)


if __name__ == "__main__":
    test_basic()
    test_list()
    test_dict()
