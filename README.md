# spotify-cli
*Control Spotify playback on any device through the command line!*


## architecture
- cloud functions
	- auth login (w/ portal)
		- finish / fail - redirect to github
	- auth refresh

- Spotify handler
	- manage auth
		- access & refresh
		- [optional] additional auth scopes (i.e. playlists, etc)
	- handle API requests (w/ auth)
	- search handler (class - stateful)
			- list results (can be non-interactive)
			- some sort of UI for going through search results (1-5, next/prev)
					- could use [PyInquirer](https://github.com/CITGuru/PyInquirer)
			- support for playlists, albums, etc

- cli
	- 100% API
	- commands
		- auth
			- status [default]
				- who's logged in, where file is saved
			- login
			- refresh ?
				- helper function
		- status
			- current song, album, device, etc
		- browse
			- open current album in browser
		- playback (actual commands below)
			- play, pause, next, prev/back, shuffle
		- ls/list
			- current album
		- search
			- interactive
			- specify --song, --album, --artist, --playlist, etc

## nice to haves
- pretty printing
- docs
- emojis

## references
- [py cli](https://medium.com/@isaac.d.adams/creating-a-cli-with-python-and-node-js-631dfaf6a879)
