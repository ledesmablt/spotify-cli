import click

from ..utils import Spotify
from ..utils.parsers import *
from ..utils.functions import format_duration_ms
from ..utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.option(
    '-v', '--verbose', count=True,
    help='Output more info (repeatable flag).'
)
@click.option(
    '--raw', is_flag=True,
    help='Output raw API response.'
)
def status(verbose=0, raw=False, _override={}, _return_parsed=False):
    """Describe the current playback session."""
    res = Spotify.request('me/player', method='GET')
    if not res:
        raise NoPlaybackError

    if raw:
        if verbose >= 0:
            import json
            click.echo(json.dumps(res))

        return res

    # raw
    data = {}
    data['is_podcast'] = res['currently_playing_type'] == 'episode'
    if data['is_podcast']:
        raise PodcastNotSupported

    data['is_shuffle'] = res['shuffle_state']
    data['repeat_state'] = res['repeat_state']
    data['is_playing'] = res['is_playing']
    data['device'] = {
        'name': res['device']['name'],
        'type': res['device']['type'],
        'volume': res['device']['volume_percent'],
    }
    item = res['item']
    context = parse_context(res['context'])

    data['music'] = {
        'context': context,
        'track': parse_track(item),
        'album': parse_album(item['album']),
        'artist': parse_artists(item['artists']),
    }
    music = data['music']
    music['track']['progress'] = format_duration_ms(res['progress_ms'])

    # parsed
    if _override:
        data.update(_override)

    # artist: name, id, url return first entry
    for key in ['name', 'id', 'url']:
        music['artist'][key] = music['artist'][key + 's'][0]
        music['artist']['long_' + key] = ', '.join(music['artist'][key + 's'])
        if key != 'name':
            music['artist']['long_' + key] = (
                music['artist']['long_' + key].replace(' ', '')
            )

    playback_status = 'Playing' if data['is_playing'] else 'Paused'
    playback_options = []
    if data['repeat_state'] == 'track':
        playback_options.append('repeat [track]')
    elif data['repeat_state'] == 'context':
        playback_options.append('repeat')

    if data['is_shuffle']:
        playback_options.append('shuffle')
    playback_str = ''
    if data['is_playing']:
        playback_options_str = '{}'.format(
            'on {}'.format(' and '.join(playback_options) + ', ')
            if playback_options else ''
        )
        playback_str = "({}{}% volume)".format(
            playback_options_str, data['device']['volume']
        )

    if _return_parsed:
        return data

    # output
    if not verbose:
        click.echo(
            '{}: {}{}\n'
            '         {} - {}'
            .format(
                playback_status,
                ' ' if not data['is_playing'] else '',
                music['track']['name'],
                music['artist']['long_name'],
                music['album']['name']
            )
        )

    if verbose >= 1:
        click.echo(
            'Track   {} ({} / {})\n'
            'Artist  {}\n'
            'Album   {}\n'
            'Status  {} {}'
            .format(
                music['track']['name'],
                music['track']['progress'],
                music['track']['duration'],
                music['artist']['long_name'],
                music['album']['name'],
                playback_status,
                playback_str
            )
        )

    if verbose >= 2:
        click.echo(
            '\n'
            'Device  {} ({})\n'
            'URL     {}'
            .format(
                data['device']['name'],
                data['device']['type'],
                music['track']['url']
            )
        )

    return
