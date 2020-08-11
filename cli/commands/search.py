import time

import click

from ..utils import Spotify
from ..utils.parsers import *
from ..utils.functions import cut_string
from ..utils.exceptions import *


@click.command(options_metavar='[<options>]')
@click.option(
    '--track', 'search_type', flag_value='track', default=True,
    help='(default) Search for a track.'
)
@click.option(
    '--album', 'search_type', flag_value='album',
    help='Search for an album'
)
@click.option(
    '--artist', 'search_type', flag_value='artist',
    help='Search for an artist.'
)
@click.option(
    '--playlist', 'search_type', flag_value='playlist',
    help='Search for a playlist'
)
@click.option(
    '-l', '--limit', type=int, default=10,
    help='Number of items to show.',
    metavar='<int>'
)
@click.option(
    '--raw', is_flag=True,
    help='Output raw API response.'
)
@click.argument(
    'keyword', type=str, metavar='<keyword>',
    nargs=-1, required=True
)
def search(
    keyword, search_type='all',
    raw=False, limit=10, _return_parsed=False
):
    """Search for any Spotify content."""
    import urllib.parse as ul
    from tabulate import tabulate

    keyword = ' '.join(keyword)
    pager = Spotify.Pager(
        'search',
        limit=limit,
        params={
            'q': ul.quote_plus(keyword),
            'type': search_type,
        },
        content_callback=lambda c: c[search_type+'s'],
    )
    if raw:
        import json
        click.echo(json.dumps(pager.content))
        return pager.content

    commands = {
        0: ['[p]lay', '[q]ueue', '[s]ave'],
        1: '[Ctrl+C] exit\n',
    }
    if search_type == 'artist':
        commands[0] = ['[s]ave']
    elif search_type == 'playlist':
        commands[0] = ['[p]lay', '[s]ave']

    headers, colalign = _get_headers(search_type)
    headers.insert(0, '#')
    if colalign:
        colalign.insert(0, 'right')

    click.echo(
        '\nSearch results for "{}"'
        .format(keyword, int(pager.offset / pager.limit) + 1)
    )
    parsed_content = {}
    end_search = False

    print_table = True
    while not end_search:
        table = []
        for i, item in enumerate(pager.content['items']):
            index = pager.offset + 1 + i
            parsed_item = _parse(item, index, search_type)
            parsed_content[index] = parsed_item
            row = [parsed_item[h] for h in headers]
            table.append(row)

        if len(table) == 0:
            click.echo('No data available for your search query.', err=True)
            return

        click.echo('\n', nl=False)
        if print_table:
            click.echo(tabulate(table, headers=headers, colalign=colalign))

        response = click.prompt(
            '\nActions:\n'
            '[n]ext/[b]ack\n'
            '{} #[,...]\n'
            '{}'
            .format(
                '/'.join(commands[0]),
                commands.get(1, '')
            )
        ).lower()

        # if any error in the middle, do not print table
        print_table = False

        cmd = response.split(' ')[0]
        if cmd == 'n':
            try:
                pager.next()
            except PagerLimitReached:
                click.echo('\nThere are no more results to display.')
                continue

        elif cmd == 'b':
            try:
                pager.previous()
            except PagerPreviousUnavailable:
                click.echo('\nYou are already at the first page.')
                continue
        else:
            # parse selection
            try:
                indices_str = response.split(' ')[1]
            except IndexError:
                _display_input_err()
                continue

            indices = indices_str.split(',')
            selected = []
            for i in indices:
                try:
                    selected.append(parsed_content[int(i)])
                except (ValueError, IndexError, KeyError):
                    continue

            # parse command
            click.echo('\n', nl=False)
            if len(selected) == 0:
                _display_input_err()
                continue

            try:
                conf_msg = _get_conf_msg(cmd, search_type, indices_str)
            except InvalidInput as e:
                click.echo(e.message, err=True)
                continue

            conf = click.confirm(conf_msg, default=True)
            if not conf:
                pass

            elif cmd == 'p':
                from cli.commands.play import play
                req_data = _format_play_req(selected, search_type)
                play.callback(data=req_data, quiet=True)
                click.echo(
                    'Now playing: {}'
                    .format(selected[0][search_type.capitalize()])
                )

            elif cmd == 'q':
                requests = _format_queue_reqs(selected, search_type)
                Spotify.multirequest(requests, delay_between=0.1)
                click.echo(
                    '{} {}/s queued.'
                    .format(len(selected), search_type)
                )

            elif cmd == 's':
                requests = _format_save_reqs(selected, search_type)
                reqs = Spotify.multirequest(requests)
                click.echo(
                    '{} {}/s saved.'
                    .format(len(selected), search_type)
                )

            print_table = True
            end_search = not click.confirm(
                '\nContinue searching?', default=True
            )

    return


def _get_headers(search_type):
    if search_type == 'track':
        return [['Track', 'Artist'], None]
    elif search_type == 'album':
        return [['Album', 'Artist', '# of tracks'], None]
    elif search_type == 'artist':
        return [
            ['Artist', 'Genre', 'Followers'],
            ['left', 'left', 'right']
        ]
    elif search_type == 'playlist':
        return [['Playlist', 'Created by', '# of tracks'], None]


def _get_conf_msg(cmd, search_type, indices_str):
    mapping = {
        'p': {
            'track': (
                'Play the selected track/s? ({})'
                .format(indices_str)
            ),
            'album': (
                'Play the selected album? ({})'
                .format(indices_str.split(',')[0])
            ),
            'playlist': (
                'Play the selected playlist? ({})'
                .format(indices_str.split(',')[0])
            ),
        },
        'q': {
            'track': (
                'Queue the selected track/s? ({})'
                .format(indices_str)
            ),
            'album': (
                'Queue the selected album? ({})'
                .format(indices_str.split(',')[0])
            ),
            'playlist': (
                'Queue the selected playlist? ({})'
                .format(indices_str.split(',')[0])
            ),
        },
        's': {
            'track': (
                'Save the selected track/s? ({})'
                .format(indices_str)
            ),
            'artist': (
                'Save the selected artist/s? ({})'
                .format(indices_str)
            ),
            'album': (
                'Save the selected album/s? ({})'
                .format(indices_str)
            ),
            'playlist': (
                'Save the selected playlist/s? ({})'
                .format(indices_str)
            ),
        }
    }
    cmd_map = mapping.get(cmd)
    if not cmd_map:
        raise InvalidInput('\nCommand [{}] not found.'.format(cmd))

    output = cmd_map.get(search_type)
    if not output:
        raise InvalidInput(
            '\nCommand not supported for {} search.'
            .format(search_type)
        )
    else:
        return output


def _parse(item, index, search_type):
    if search_type == 'track':
        item = parse_track_item_full(item)
        output = {
            'Track': cut_string(item['track']['name'], 50),
            'Artist': cut_string(', '.join(item['artists']['names']), 30),
            'uri': item['track']['uri'],
            'id': item['track']['id'],
            'context_uri': item['album']['uri'],
            'track_number': item['track']['track_number'],
        }
    elif search_type == 'album':
        output = {
            'Album': cut_string(item['name'], 50),
            'Artist': cut_string(
                ', '.join([a['name'] for a in item['artists']]), 30
            ),
            '# of tracks': item.get('total_tracks', 0),
            'uri': item['uri'],
            'id': item['id'],
        }
    elif search_type == 'artist':
        output = {
            'Artist': item['name'],
            'Genre': cut_string(', '.join(item.get('genres', '')), 30),
            'Followers': '{:,}'.format(item['followers'].get('total', 0)),
            'uri': item['uri'],
            'id': item['id'],
        }
    elif search_type == 'playlist':
        output = {
            'Playlist': cut_string(item['name'], 50),
            'Created by': cut_string(
                item['owner'].get('display_name'), 30
            ),
            '# of tracks': item['tracks'].get('total', 0),
            'uri': item['uri'],
            'id': item['id'],
        }

    output['#'] = index
    return output


def _format_play_req(selected, search_type):
    if search_type == 'track':
        if len(selected) == 1:
            return {
                'context_uri': selected[0]['context_uri'],
                'offset': {
                    'uri': selected[0]['uri'],
                },
            }
        else:
            return {
                'uris': [track['uri'] for track in selected],
            }

    elif search_type in ['album', 'playlist']:
        return {
            'context_uri': selected[0]['uri']
        }


def _format_queue_reqs(selected, search_type):
    if search_type == 'track':
        return [
            {
                'endpoint': 'me/player/queue?uri=' + s['uri'],
                'method': 'POST',
            }
            for s in selected
        ]

    elif search_type == 'album':
        album = spotify.request('albums/' + selected[0]['id'])
        return [
            {
                'endpoint': 'me/player/queue?uri=' + track['uri'],
                'method': 'post',
            }
            for track in album['tracks']['items']
        ]


def _format_save_reqs(selected, search_type):
    base_req = {
        'method': 'PUT',
        'handle_errs': {
            403: (AuthScopeError, {'required_scope_key': 'user-modify'})
        }
    }
    requests = []
    for s in selected:
        r = base_req.copy()
        if search_type in ['track', 'album']:
            r['endpoint'] = 'me/{}s?ids={}'.format(search_type, s['id'])
        elif search_type == 'artist':
            r['endpoint'] = (
                'me/following?type=artist&ids={}'
                .format(s['id'])
            )
        elif search_type == 'playlist':
            r['endpoint'] = 'playlists/{}/followers'.format(s['id'])
            r['data'] = {'public': True}

        requests.append(r)

    return requests


def _display_input_err():
    click.echo(
        'Input error! Please try again.\n'
        'Format: <command> <#s comma delimited>\n'
        'Example: q 3,2,1',
        err=True
    )
