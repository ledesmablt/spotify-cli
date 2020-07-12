import click


#auth
class AuthorizationError(click.ClickException):
    def __init__(self):
        self.message = 'CLI not authenticated. (spotify auth login)'
        super().__init__(self.message)

class TokenExpired(click.ClickException):
    def __init__(self):
        """Signals a token refresh."""
        pass


# playback
class NoPlaybackError(click.ClickException):
    def __init__(self):
        self.message = 'No playback session detected. Please start Spotify on one of your devices.'
        super().__init__(self.message)

class PodcastNotSupported(click.ClickException):
    def __init__(self):
        self.message = 'Podcasts are currently not supported. This feature is in development.'
        super().__init__(self.message)
