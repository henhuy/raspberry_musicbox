import os
from vlc import MediaListPlayer, MediaList, Media, MediaPlayer
import logging
from itertools import cycle

DEBUG = True
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

from spotipy.client import SpotifyException
from sp import SpotipyPlayer
from read_musiclist import get_musiclist, MusicType
from settings import DATA_DIR

path = os.path.dirname(__file__)
music_list = get_musiclist()


class Player(object):
    possible_players = {
        MediaPlayer: [MusicType.Url],
        MediaListPlayer: [MusicType.File, MusicType.Folder],
        SpotipyPlayer: [MusicType.Spotify]
    }

    def __init__(self, music_data):
        self.current = None
        self.music_list = music_data
        self.music_indices = None
        self.current_music_index = 0
        self.player = None
        self.players = []
        self.__init_players()

    def __init_players(self):
        for p in self.possible_players:
            try:
                self.players.append(p())
            except Exception:
                logging.warning(
                    'Could not initialize player "' + str(p) + '". Music types for this player will be ignored.')

    def __set_player(self, music_type):
        success = True
        # Find corresponding player type:
        player_type = next((key for key, value in self.possible_players.items() if music_type in value), None)
        if player_type is None:
            logging.warning('Player for music type "' + str(music_type) + '" not found')
            success = False
        else:
            if isinstance(self.player, player_type):
                self.stop()
            else:
                # Activate player if it could be initialized beforehand:
                found_player = next((p for p in self.players if isinstance(p, player_type)), None)
                if found_player is None:
                    logging.warning(
                        'Player for music type "' + str(music_type) + '" has not been initialized while startup.')
                    success = False
                else:
                    self.stop()
                    self.player = found_player
        return success

    def next(self):
        if self.player is None:
            return
        if isinstance(self.player, SpotipyPlayer):
            self.player.next()
            return
        if self.music_list[self.current].type == MusicType.Url:
            logging.info('Cannot skip radio stream tracks')
            return
        if len(self.music_list[self.current].items) == 1:
            logging.info('Single music item is already running')
            return
        if self.music_indices:
            self.player.play_item_at_index(next(self.music_indices))
            return

        status = self.player.next()
        if status == -1:
            self.player.next()

    def stop(self):
        if self.player is None:
            return
        if isinstance(self.player, MediaListPlayer):
            self.player.stop()
        else:
            try:
                self.player.stop()
            except SpotifyException:
                pass

    def __play_music(self, music_item):
        self.music_indices = None
        if music_item.type == MusicType.File:
            music_files = [os.path.join(DATA_DIR, item) for item in music_item.items]
            self.player.set_media_list(MediaList(music_files))
            self.player.play()
        elif music_item.type == MusicType.Url:
            stream = Media(music_item.items)
            stream.get_mrl()
            self.player.set_media(stream)
            self.player.play()
        elif music_item.type == MusicType.Folder:
            song_list = []
            count_index = 0
            music_indices = []
            for music_folder in music_item.items:
                music_indices.append(count_index)
                music_folder_path = os.path.join(DATA_DIR, music_folder)
                try:
                    music_files = os.listdir(music_folder_path)
                except FileNotFoundError:
                    logging.error("Could not find music folder at '%s'", music_folder)
                    continue
                count_index += len(music_files)
                song_list.extend(
                    sorted(os.path.join(music_folder_path, file) for file in music_files)
                )
            self.music_indices = cycle(music_indices)
            next(self.music_indices)
            self.player.set_media_list(MediaList(song_list))
            self.player.play()
        elif music_item.type == MusicType.Spotify:
            if music_item.items is None:
                self.player.play()
            else:
                self.player.play(music_item.items)
        
    def play(self, rfid):
        music_item = self.music_list.get(rfid)
        if music_item is None:
            return
        if self.current == rfid:
            self.next()
            return

        if not self.__set_player(music_item.type):
            return

        logging.info('Load music file: ' + str(music_item))
        self.__play_music(music_item)
        self.current = rfid


player = Player(music_list)
player.play('DEFAULT')

try:
    while True:
        rfid_data = input('Please enter music entry:')
        if rfid_data == 'list':
            print(music_list)
            continue
        if rfid_data not in music_list:
            logging.warning('Could not find data for RFID #' + str(rfid_data))
        else:
            player.play(rfid_data)
except KeyboardInterrupt:
    player.stop()
