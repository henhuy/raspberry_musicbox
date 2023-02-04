
from configparser import ConfigParser
from collections import namedtuple
from enum import Enum
import logging

from settings import MUSIC_LIST

MusicItem = namedtuple('MusicItem', ['name', 'type', 'items', 'track_mode'])

DEFAULT_TRACK_MODE = "single"


class TrackMode(Enum):
    Single = "single"
    Album = "album"

    @classmethod
    def find_type(cls, item):
        for attr in cls:
            if attr.value == item:
                return attr
        raise KeyError("There is no track mode '%s'", item)


class MusicType(Enum):
    File = 'file'
    Folder = 'folder'
    Url = 'url'
    Spotify = 'spotify'

    @classmethod
    def find_type(cls, item):
        for attr in cls:
            if attr.value == item:
                return attr
        raise KeyError


def get_musiclist(file=MUSIC_LIST):
    config = ConfigParser()
    config.read(file)
    music_list = {}

    for rfid_key in config:
        name = config[rfid_key].get('name')
        music_type_str = config[rfid_key].get('type')
        items = config[rfid_key].get('items')
        track_mode = TrackMode.find_type(config[rfid_key].get('track_mode', DEFAULT_TRACK_MODE))
        if any([name, music_type_str, items]) is None:
            logging.warning('Could not import music item for rfid key #' + rfid_key)
            continue

        try:
            music_type = MusicType.find_type(music_type_str)
        except KeyError:
            logging.warning('Could not detect music type for rfid key #' + rfid_key)
            continue

        # Create list of items in case of folder or file type:
        if music_type in (MusicType.File, MusicType.Folder):
            items = items.split(",")

        music_list[rfid_key] = MusicItem(name, music_type, items, track_mode)

    return music_list
