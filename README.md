# Raspberry Musicbox

MusicBox for raspberry pi, music is controlled by rfid chip reader

Musicbox uses vlc-player and spotify to play music.
Player is controlled by RFID chip card.

## Configuration

Music files, folders and urls are read in from config file (defaults to "./music.cfg").
`ConfigParser` is used to read in configuration.
Structure of music configuration must look as follows:

```
[<RFID of card reader>]
    name = <Custom name>
    type = <file/folder/url/spotify>
    items = <url or comma-separated-list-of-files-or-folders>
    track_mode = <optional, "single" or "album", defaults to "single">
```

Config must hold section with RFID "DEFAULT", which played at startup.

## Environment Variables

You can set following variables:
* `MUSIC_LIST`: Path to file to read in music items (defaults to "./music.cfg") 
* `MUSIC_DATA_PATH_`: Path where music folders are located (defaults to "./data") 

## Requirements

You must install VLC player
```bash
sudo apt-get install vlc
```
