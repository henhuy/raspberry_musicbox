
from configparser import ConfigParser
from collections import namedtuple
from enum import Enum
import logging

from settings import MUSIC_LIST

MusicItem = namedtuple('MusicItem', ['name', 'type', 'items'])


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
        return None


def get_musiclist(file=MUSIC_LIST):
    config = ConfigParser()
    config.read(file)
    music_list = {}

    for rfid_key in config:
        name = config[rfid_key].get('name')
        music_type_str = config[rfid_key].get('type')
        items = config[rfid_key].get('items').split(",")
        if any([name, music_type_str, items]) is None:
            logging.warning('Could not import music item for rfid key #' + rfid_key)
            continue

        try:
            music_type = MusicType.find_type(music_type_str)
        except KeyError:
            logging.warning('Could not detect music type for rfid key #' + rfid_key)
            continue

        music_list[rfid_key] = MusicItem(name, music_type, items)

    return music_list
