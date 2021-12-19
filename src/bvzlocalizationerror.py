class LocalizationError(Exception):
    """
    Localization exception
    """

    def __init__(self, message, errno=0):

        super(LocalizationError, self).__init__()

        self.code = errno
        self.message = message

    @property
    def errno(self):
        return self.code
