class CouldNotVoteException(Exception):
    def __init__(self, event=None, reason=None):
        self.event = event
        self.reason = reason
