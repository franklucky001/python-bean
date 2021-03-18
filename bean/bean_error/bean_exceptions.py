# -*- coding:utf-8 -*-]
from collections import deque


class BeanValidationError(Exception):

    def __init__(self,
                 message,
                 exception_path=(),
                 context=(),
                 parent=None):
        super(BeanValidationError, self).__init__(message, exception_path, context, parent)
        self.message = message
        self.exception_path = deque(exception_path)
        self.relative_exception_path = self.exception_path
        self.context = list(context)
        for error in context:
            error.parent = self
        self.parent = parent

    @property
    def absolute_path(self):
        parent = self.parent
        if parent is None:
            return self.exception_path

        path = deque(self.exception_path)
        parent_path = deque(parent.absolute_path)
        path.extend(parent_path)
        return path


class BeanValueError(BeanValidationError):

    def __init__(self,
                 message,
                 exception_path=(),
                 context=(),
                 parent=None):
        super(BeanValueError, self).__init__(message, exception_path, context, parent)


class BeanAssertError(BeanValidationError):

    def __init__(self,
                 message,
                 exception_path=(),
                 context=(),
                 parent=None):
        super(BeanAssertError, self).__init__(message, exception_path, context, parent)
