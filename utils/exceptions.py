class AuthorizationError(Exception):
    def __init__(self):
        self.message = 'Please authenticate the CLI (spotify auth login)'
        super().__init__(self.message)
