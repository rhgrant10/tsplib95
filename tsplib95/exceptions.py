# -*- coding: utf-8 -*-


class TsplibError(Exception):
    pass


class ValidationError(TsplibError):
    pass


class ParsingError(TsplibError, ValueError):
    pass
