# -*- coding: utf-8 -*-
"""
parsedatetime/context_stack.py

Class handling the stack of contexts
"""

from threading import local


class ContextStack(object):
    """
    A thread-safe stack to store context(s)

    Internally used by L{Calendar} object
    """

    def __init__(self):
        self.__local = local()

    @property
    def __stack(self):
        if not hasattr(self.__local, 'stack'):
            self.__local.stack = []
        return self.__local.stack

    def push(self, ctx):
        self.__stack.append(ctx)

    def pop(self):
        try:
            return self.__stack.pop()
        except IndexError:
            return None

    def last(self):
        try:
            return self.__stack[-1]
        except IndexError:
            raise RuntimeError('context stack is empty')

    def isEmpty(self):
        return not self.__stack
