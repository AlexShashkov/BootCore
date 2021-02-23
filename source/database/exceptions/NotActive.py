class NotActive(Exception):
    def __init__(self, message='User is not active'):
        super().__init__(message)