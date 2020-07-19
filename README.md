# Spotify CLI 🎧

Control Spotify playback on any device through the command line.

## Installation

This package only supports Python 3 and above.
```
pip3 install spotify-cli
```

## Usage

This CLI performs all interactions through the Spotify API. All you need is a stable internet connection and an active Spotify session on any device.

Authorize the CLI & save your credentials locally.
```
spotify auth login
```

Start Spotify playback on any device and run the `spotify` command.
```
> spotify
Usage: spotify [<options>] <command>

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  auth      Manage user authentication for spotify-cli.
  devices   Manage active devices.
  next      Play the next song in the queue.
  pause     Pause current playback.
  play      Resume current playback.
  previous  Play the previous song in the queue.
  status    Display info about the current playback session.
  volume    Control the active device's volume level.
```

## Examples

Describe and control current playback.
```
> spotify play
Playing: Nights
         Frank Ocean - Blonde

> spotify status -vv
Song    Nights (03:31 / 05:07)
Artist  Frank Ocean
Album   Blonde
Status  Playing (on repeat, 60% volume)

Device  Lorenzo (Smartphone)
URL:    https://open.spotify.com/track/7eqoqGkKwgOaWNNHx90uEZ

> spotify vol --up 20
Volume set to 80%

> spotify vol --to 100
Volume set to 100%
```

You can also manage multiple devices.
```
❯ spotify devices -v
  LENOVO - Computer
* Lorenzo - Smartphone
  Web Player (Chrome) - Computer

❯ spotify devices --switch comp
2 devices matched "comp".
? Please select the device to activate.
 > LENOVO - Computer
   Web Player (Chrome) - Computer

Switched to LENOVO - Computer
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

## Notes
- Playback and device-related commands require at least one active Spotify session on any device.
  - You can just start and stop playback to "activate" your device.
  - Your device will remain "active" even when paused.
- Some operations may not be supported on certain devices (i.e. volume control for mobile).
- Behavior may differ for users not subscribed to Spotify Premium.
- In development: search, browse, more playback options, custom auth scopes.

## [License](LICENSE)

The MIT License (MIT)  
Copyright (c) 2020 Benj Ledesma