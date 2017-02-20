

class GsmModemError(Exception):
    pass


class CancelError(GsmModemError):
    pass


class AtError(GsmModemError):
    pass


class NoReplyAtError(AtError):
    pass


class UssdError(AtError):
    pass


class NoReplyUssdError(UssdError):
    pass


class UnexpectedReplyUssdError(UssdError):
    pass


class OperationNotSupportedUssdError(UssdError):
    pass


class DeviceUssdError(UssdError):
    pass


class CsqError(AtError):
    pass


class CallError(AtError):
    pass


class SmsError(AtError):
    pass


class UnexpectedReplySmsError(SmsError):
    pass


class NoReplySmsError(SmsError):
    pass
