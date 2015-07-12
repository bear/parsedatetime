# -*- coding: utf-8 -*-

from threading import local


class pdtContextStack(object):

    def __init__(self):
        self.__local = local()
        self.__local.stack = []

    def push(self, ctx):
        self.__local.stack.append(ctx)

    def pop(self):
        try:
            return self.__local.stack.pop()
        except IndexError:
            return None

    def last(self):
        try:
            return self.__local.stack[-1]
        except IndexError:
            raise RuntimeError('context stack is empty')

    def isEmpty(self):
        return not self.__local.stack


class pdtContext(object):

    __slots__ = ('hasTime', 'hasDate')

    def __init__(self, hasTime=False, hasDate=False):
        self.hasTime = hasTime
        self.hasDate = hasDate

    def update(self, context):
        self.hasTime = self.hasTime or context.hasTime
        self.hasDate = self.hasDate or context.hasDate

    @property
    def dateTimeFlag(self):
        return int(self.hasDate and 1) | int(self.hasTime and 2)

    @property
    def hasDateOrTime(self):
        return self.hasDate or self.hasTime

    def __repr__(self):
        return ('pdtContext(hasTime=%s, hasDate=%s)' %
                (self.hasTime, self.hasDate))

    def __eq__(self, ctx):
        return (self.hasTime == ctx.hasTime and
                self.hasDate == ctx.hasDate)
