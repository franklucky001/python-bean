# -*- coding:utf-8 -*-
from bean.model.bean_model import BeanModel
from bean.bean_error import BeanValidationError
from bean.fields import IntField, StringField, ArrayField, ObjectField


class Friend(BeanModel):
    name = StringField()
    age = IntField(minimum=1, maximum=100)


class Family(BeanModel):
    father = StringField()
    mother = StringField()
    members = IntField(minimum=1, maximum=10, default=3)


class User(BeanModel):
    name = StringField()
    age = IntField(required=True, minimum=1, maximum=100)
    friends = ArrayField(items=[Friend()])
    family = ObjectField(required=True,
                         properties={'father': StringField(), 'mother': StringField(), 'members': IntField()})


if __name__ == "__main__":
    import sys
    data = {
        "name": "mike",
        "age": "20",
        "friends": [{"name": "lily", "age": "18"}],
        "family": {"father": "mike's dad", "mother": "mike's mom"}
    }
    user_1 = User()
    try:
        user_1.bind(data)
    except BeanValidationError as e:
        src = '.'.join(e.absolute_path)
        print(e.message, f"caused by {src}")
        sys.exit(-1)
    print(user_1.value)
    # print(user_1.model_value)
    # print(user_1.family.value)
