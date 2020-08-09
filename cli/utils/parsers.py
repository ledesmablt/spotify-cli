"""Functions for parsing Spotify API objects."""
from .functions import *


def parse_track(track):
    return {
        'name': track['name'],
        'id': track['id'],
        'url': track['external_urls']['spotify'],
        'api': track['href'],
        'uri': track['uri'],
        'track_number': track['track_number'],
        'duration': format_duration_ms(track['duration_ms']),
    }


def parse_album(album):
    return {
        'name': album['name'],
        'id': album['id'],
        'url': album['external_urls']['spotify'],
        'api': album['href'],
        'uri': album['uri'],
        'release_date': album['release_date'],
        'total_tracks': album['total_tracks'],
    }


def parse_artists(artists):
    assert type(artists) == list
    return {
        'names': [a['name'] for a in artists],
        'ids': [a['id'] for a in artists],
        'urls': [a['external_urls']['spotify'] for a in artists],
    }


def parse_context(context):
    # playback context not available if private session or unnamed playlist
    if not context:
        return {'type': None}

    return {
        'type': context['type'],
        'id': context['href'].split('/')[-1],
        'url': context['external_urls']['spotify'],
        'api': context['href'],
        'uri': context['uri'],
    }


def parse_track_item_full(item):
    return {
        'track': parse_track(item),
        'album': parse_album(item['album']),
        'artists': parse_artists(item['artists']),
    }
