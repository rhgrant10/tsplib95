

class TsplibError(Exception):
    pass


class ValidationError(TsplibError):
    pass


class ParsingError(TsplibError):
    pass
