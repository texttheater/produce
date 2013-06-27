class UserError(Exception):

    """
    An error that should be caught in the main program and lead to display of
    the error message, then to immediate exit of the program with a non-0 
    status code
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class ProducefileError(UserError):

    """
    Error in the Producefile.
    """

    def __init__(self, line, message):
        self.line = line
        UserError.__init__(self, message)

    def __str__(self):
        return 'Line %d: %s' % (self.line, self.message)
