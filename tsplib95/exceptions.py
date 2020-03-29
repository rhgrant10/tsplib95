# -*- coding: utf-8 -*-


class TsplibError(Exception):

    @classmethod
    def wrap(cls, exc, message):
        message = f'{message}: {exc.args[0]}'
        return cls(message, *exc.args[1:])

    def ammend(self, message):
        new_message = f'{message}: {self.args[0]}'
        new_args = [new_message] + list(self.args[1:])
        self.args = tuple(new_args)
        return self  # for easy raise syntax


class ValidationError(TsplibError):
    pass


class ParsingError(TsplibError, ValueError):
    pass


class RenderingError(TsplibError, ValueError):
    pass
