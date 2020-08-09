"""Custom exceptions."""
from click import ClickException


# auth
class AuthorizationError(ClickException):
    def __init__(self):
        self.message = (
            'CLI not authenticated.\n'
            'Please run the command - spotify auth login'
        )
        super().__init__(self.message)


class AuthScopeError(ClickException):
    def __init__(self, required_scope_key):
        from cli.utils.constants import AUTH_SCOPES_MAPPING
        try:
            required_scope_msg = next(filter(
                lambda scope: scope['value'] == required_scope_key,
                AUTH_SCOPES_MAPPING
            ))['name']
        except (IndexError, KeyError):
            raise Exception('Scope key not found')

        self.message = (
            'Operation restricted for currently authorized scopes.\n'
            'Please run the command - spotify auth login\n\n'
            'Required scopes:\n'
            '> {}'
            .format(required_scope_msg)
        )
        super().__init__(self.message)


class TokenExpired(ClickException):
    def __init__(self):
        """Signals a token refresh."""
        pass


# api
class SpotifyAPIError(ClickException):
    def __init__(self, message, status):
        self.message = 'Spotify API - {} {}'.format(status, message)
        self.status = status
        super().__init__(self.message)


# playback
class NoPlaybackError(ClickException):
    def __init__(self):
        self.message = (
            'No playback session detected.\n'
            'Please start Spotify on one of your devices.'
        )
        super().__init__(self.message)


class InvalidVolumeInput(ClickException):
    def __init__(self):
        self.message = (
            'Please specify a valid volume option and amount.\n'
            'Example: spotify volume up 15'
        )
        super().__init__(self.message)


class DeviceOperationRestricted(ClickException):
    def __init__(self):
        self.message = 'Operation restricted for the active device.'
        super().__init__(self.message)


# misc
class FeatureInDevelopment(ClickException):
    def __init__(self):
        self.message = (
            'This feature is currently in development.\n'
            'Info: https://github.com/ledesmablt/spotify-cli'
        )
        super().__init__(self.message)


class PodcastNotSupported(ClickException):
    def __init__(self):
        self.message = 'Podcasts are not supported.'
        super().__init__(self.message)


class ConnectionError(ClickException):
    def __init__(self):
        self.message = (
            'Could not establish an internet connection.\n'
            'Please connect and try again.'
        )
        super().__init__(self.message)


class InvalidInput(ClickException):
    def __init__(self, helpmsg=''):
        self.message = 'Invalid input!' + helpmsg
        super().__init__(self.message)


class PagerLimitReached(Exception):
    """Results limit reached."""
    pass


class PagerPreviousUnavailable(Exception):
    """Previous page not available."""
    pass
