class NoSlots(Exception):
    def __init__(self, reason=None):
        self.reason = reason


class InvalidInput(Exception):
    def __init__(self, reason=None):
        self.reason = reason


class MaxLength(Exception):
    def __init__(self, reason=None):
        self.reason = reason


class MultipleBookings(Exception):
    def __init__(self, reason=None):
        self.reason = reason


class TooShortNotice(Exception):
    def __init__(self, reason=None):
        self.reason = reason
