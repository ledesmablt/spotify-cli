import click

class AuthorizationError(click.ClickException):
    def __init__(self):
        self.message = 'CLI not authenticated. (spotify auth login)'
        super().__init__(self.message)

class NoPlaybackError(click.ClickException):
    def __init__(self):
        self.message = 'No playback session detected. Please start Spotify on one of your devices.'
        super().__init__(self.message)
