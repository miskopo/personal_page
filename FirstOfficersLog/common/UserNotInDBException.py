class UserNotInDBException(Exception):
    def __init__(self):
        super(UserNotInDBException, self).__init__()