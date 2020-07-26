from click import ClickException


# auth
class AuthorizationError(ClickException):
    def __init__(self):
        self.message = 'CLI not authenticated.\nPlease run the command - spotify auth login'
        super().__init__(self.message)

class AuthScopeError(ClickException):
    def __init__(self, required_scope_key):
        from cli.utils.constants import AUTH_SCOPES_MAPPING
        try:
            required_scope_msg = next(filter(
                lambda scope: scope['value'] == required_scope_key,
                AUTH_SCOPES_MAPPING
            ))['name']
        except:
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

class SpotifyAPIError(ClickException):
    def __init__(self, message, status):
        self.message = 'Spotify API - {} {}'.format(status, message)
        self.status = status
        super().__init__(self.message)


# playback
class NoPlaybackError(ClickException):
    def __init__(self):
        self.message = 'No playback session detected.\nPlease start Spotify on one of your devices.'
        super().__init__(self.message)

class InvalidVolumeInput(ClickException):
    def __init__(self):
        self.message = 'Please specify one volume option.\nExample: spotify volume -u 15'
        super().__init__(self.message)

class DeviceOperationRestricted(ClickException):
    def __init__(self):
        self.message = 'Operation restricted for the active device.'
        super().__init__(self.message)


# misc
class PodcastNotSupported(ClickException):
    def __init__(self):
        self.message = 'Podcasts are currently not supported. This feature is in development.'
        super().__init__(self.message)
