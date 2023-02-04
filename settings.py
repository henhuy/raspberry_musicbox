
import os
import logging

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.environ.get("MUSIC_DATA_PATH", os.path.join(ROOT_DIR, "data"))

MUSIC_LIST = os.environ.get("MUSIC_LIST", os.path.join(ROOT_DIR, "music.cfg"))


logging.info("Using music list from file: %s", MUSIC_LIST)
logging.info("Using path '%s' as data folder.", DATA_DIR)
