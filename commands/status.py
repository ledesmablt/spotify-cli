import os
import json
import time
from uuid import uuid1

import click
import requests

from utils import Spotify
from utils.constants import AUTH_URL, CREDS_PATH 
from utils.exceptions import *
from utils.functions import format_duration_ms


@click.command()
@click.option('-v', '--verbose', count=True)
@click.option('--raw', is_flag=True)
def status(verbose, raw):
    res = Spotify.request('me/player', method='GET')
    if raw:
        click.echo(res)
        return

    if not res:
        raise NoPlaybackError

    # raw
    data = {}
    data['is_podcast'] = res['currently_playing_type'] == 'episode'
    if data['is_podcast']:
        raise PodcastNotSupported

    data['is_shuffle'] = res['shuffle_state']
    data['is_repeat'] = res['repeat_state']
    data['is_playing'] = res['is_playing']
    data['device'] = {
        'name': res['device']['name'],
        'type': res['device']['type'],
    }
    item = res['item']
    data['music'] = {
        # note: playback context not available if private session or unnamed playlist
        'context': res['context'],
        'song': {
            'name': item['name'],
            'url': item['external_urls']['spotify'],
            'api': item['href'],
            'track_number': item['track_number'],
            'progress': format_duration_ms(res['progress_ms']),
            'duration': format_duration_ms(item['duration_ms']),
        },
        'album': {
            'name': item['album']['name'],
            'url': item['album']['external_urls']['spotify'],
            'api': item['album']['href'],
            'release_date': item['album']['release_date'],
        },
        'artist': {
            'name': ', '.join([artist['name'] for artist in item['artists']]),
            'urls': [artist['external_urls']['spotify'] for artist in item['artists']],
        },
    }
    music = data['music']

    # parsed
    playback_status = 'Playing' if data['is_playing'] else 'Paused'
    playback_options = []
    if data['is_repeat']:
        playback_options.append('repeat')
    if data['is_shuffle']:
        playback_options.append('shuffle')

    # output
    if not verbose:
        click.echo(
            f"{playback_status}: {' ' if not data['is_playing'] else ''}"
            f"{music['song']['name']}"
            f"\n         {music['artist']['name']} - {music['album']['name']}"
        )

    if verbose >= 1:
        click.echo('\n'.join([
            f"Song    {music['song']['name']} ({music['song']['progress']} / {music['song']['duration']})",
            f"Artist  {music['artist']['name']}",
            f"Album   {music['album']['name']}",
            f"Status  {playback_status}"
            f"""{' (on {})'.format(
                ' and '.join(playback_options) if playback_options and data['is_playing'] else ''
            )}"""
        ]))
    if verbose >= 2:
        click.echo('')
        click.echo('\n'.join([
            f"Device  {data['device']['name']} ({data['device']['type']})",
            f"URL:    {music['song']['url']}"
        ]))


    return
