# Spotify CLI 🎧

Control Spotify playback on any device through the command line.

## Installation

This package only supports Python 3 and above.
```
$ pip3 install --upgrade spotify-cli
```

## Usage

This CLI performs all interactions through the Spotify API. All you need is a stable internet connection and an active Spotify session on any device.

Authorize the CLI & save your credentials locally.
```
$ spotify auth login
```

Start Spotify playback on any device and run the `spotify` command.
```
$ spotify
Usage: spotify [<options>] <command>

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  auth      Manage user authentication for spotify-cli.
  browse    Open the current track, album, artist, or playlist in the...
  devices   Manage active devices.
  history   List your recently played tracks.
  next      Play the next track in the queue.
  pause     Pause playback.
  play      Resume playback or search for a track/album/playlist to play.
  previous  Play the previous track in the queue.
  queue     Add a track or album to your queue.
  repeat    Turn repeat on (all/track) or off.
  save      Save a track, album, artist, or playlist.
  search    Search for any Spotify content.
  shuffle   Turn shuffle on or off.
  status    Describe the current playback session.
  top       List your top tracks or artists.
  volume    Control the active device's volume level (0-100).
```

## Examples

Describe and control current playback.
```
$ spotify play
Playing: Nights
         Frank Ocean - Blonde

$ spotify status -vv
Track   Nights (03:31 / 05:07)
Artist  Frank Ocean
Album   Blonde
Status  Playing (on repeat, 60% volume)

Device  Lorenzo (Smartphone)
URL:    https://open.spotify.com/track/7eqoqGkKwgOaWNNHx90uEZ

$ spotify vol up 20
Volume set to 80%

$ spotify vol to 100
Volume set to 100%
```

You can also manage multiple devices.
```
$ spotify devices -v
  LENOVO - Computer
* Lorenzo - Smartphone
  Web Player (Chrome) - Computer

$ spotify devices --switch comp
2 devices matched "comp".
? Please select the device to activate.
 > LENOVO - Computer
   Web Player (Chrome) - Computer

Switched to LENOVO - Computer
```

Search for a track to play, queue, or save.
```
$ spotify search red velvet

Search results for "red velvet"

  #  Track                                      Artist
---  -----------------------------------------  ---------------------------
  1  Psycho                                     Red Velvet
  2  Monster                                    Red Velvet - IRENE & SEULGI
  3  Bad Boy                                    Red Velvet
  4  빨간 맛 Red Flavor                         Red Velvet
  5  피카부 Peek-A-Boo                          Red Velvet
  6  Naughty                                    Red Velvet - IRENE & SEULGI
  7  Power Up                                   Red Velvet
  8  Dumb Dumb                                  Red Velvet
  9  Bad Boy - (English Version) [Bonus Track]  Red Velvet
 10  In & Out                                   Red Velvet

Actions:
[n]ext/[b]ack
[p]lay/[q]ueue/[s]ave #[,...]
[a]dd to playlist #[,...] <playlist>
: q 1,4,5

Queue the selected track/s? (1,4,5) [Y/n]: Y
3 track/s queued.

Continue searching? [Y/n]:
```

Some commands support search queries (`play`, `queue`, `save`).
```
$ spotify play red velvet
Playing: Psycho
         Red Velvet - ‘The ReVe Festival’ Finale

$ spotify queue --album reve finale
‘The ReVe Festival’ Finale - Red Velvet (16 tracks)
Add this album to the queue? [Y/n]: Y
Album added to queue.

$ spotify save --artist red velvet
Red Velvet
Save this artist to your library? [Y/n]: Y
Following artist - Red Velvet.
```

Command shortcut prefixes are supported.
```bash
# supported
spotify volume
spotify vol
spotify v

spotify next
spotify n

spotify previous
spotify prev

# not supported - too many matches (pause, play, previous)
spotify p
```

Some commands support the `--raw` flag to output the Spotify API JSON response (shell script-friendly).
```bash
$ spotify status --raw | jq .context
{
  "external_urls": {
    "spotify": "https://open.spotify.com/album/3mH6qwIy9crq0I9YQbOuDf"
  },
  "href": "https://api.spotify.com/v1/albums/3mH6qwIy9crq0I9YQbOuDf",
  "type": "album",
  "uri": "spotify:album:3mH6qwIy9crq0I9YQbOuDf"
}
```

## Notes
- Playback and device-related commands require at least one active Spotify session on any device.
  - You can just start and stop playback to "activate" your device.
  - Your device will remain "active" even when paused.
- Some operations may not be supported on certain devices (i.e. volume control for mobile) and for users not subscribed to Spotify Premium.

## [License](LICENSE)

The MIT License (MIT)  
Copyright (c) 2020 Benj Ledesma
