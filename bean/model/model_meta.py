# -*- coding:utf-8 -*-


class ModelMeta(type):

    def __new__(mcs, name, bases, attrs):
        if name == "BeanModel":
            return type.__new__(mcs, name, bases, attrs)
        _mappings = dict()
        from bean.fields.bean_field import BeanField
        for k, v in attrs.items():
            if isinstance(v, BeanField):
                _mappings[k] = v
        for k in _mappings.keys():
            attrs.pop(k)
        attrs["__field_mapping__"] = _mappings
        attrs["__field_name__"] = name
        return type.__new__(mcs, name, bases, attrs)
