# -*- coding: utf-8 -*-


class TsplibError(Exception):

    @classmethod
    def wrap(cls, exc, message):
        if exc.args and exc.args[0]:
            message = f'{message}: {exc.args[0]}'
        return cls(message, *exc.args[1:])

    def amend(self, message):
        return self.__class__.wrap(self, message)


class ValidationError(TsplibError):
    pass


class ParsingError(TsplibError, ValueError):
    pass


class RenderingError(TsplibError, ValueError):
    pass
