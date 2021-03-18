# -*- coding:utf-8 -*-
from bean.model.bean_model import BeanModel


class ReflectModel(BeanModel):

    def __init__(self, mappings, **kwargs):
        setattr(self, "__reflect_mapping__", mappings)
        super(ReflectModel, self).__init__(**kwargs)
