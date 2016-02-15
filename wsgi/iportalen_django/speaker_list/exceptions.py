class SpeakerListException(Exception):
    def __init__(self, reason=None):
        self.reason = reason
