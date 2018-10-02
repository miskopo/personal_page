class UserExistsException(Exception):
    def __init__(self):
        super(UserExistsException, self).__init__()