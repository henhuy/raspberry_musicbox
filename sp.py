from spotipy import client
import spotipy.util as util
import logging
from configparser import ConfigParser

DEVICE_NAME = 'pc-henner'


class SpotipyPlayer(object):
    def __init__(self):
        config = ConfigParser()
        config.read('spotify.cfg')
        credentials = dict(config['DEFAULT'])
        token = util.prompt_for_user_token(**credentials)
        self.sp = client.Spotify(auth=token)
        self.device_id = self.__find_device()
        self.sp.transfer_playback(device_id=self.device_id, force_play=False)
        self.current = None

    def __find_device(self):
        devices = self.sp.devices()
        if devices is None:
            RuntimeError('No spotify devices found')
        for dev in devices['devices']:
            if dev['name'] == DEVICE_NAME:
                return dev['id']
        logging.warning('Found devices: ' + str(devices))
        raise NameError(
            'Could not detect device "' + DEVICE_NAME + '"'
        )

    def get_tracks(self, playlist):
        if playlist == 'songs':
            results = self.sp.current_user_saved_tracks(limit=50)
        else:
            results = self.sp.user_playlist_tracks(user='henhuy', playlist_id=playlist)
        songs = []
        while True:
            for item in results['items']:
                songs.append(item['track']['uri'])
            results = self.sp.next(results)
            if results is None or results['next'] is None:
                break
        return songs

    def play(self, playlist='songs'):
        if self.current is None or self.current != playlist:
            songs = self.get_tracks(playlist)
            self.sp.start_playback(device_id=self.device_id, uris=songs)
            self.current = playlist
        else:
            self.sp.start_playback(device_id=self.device_id)

    def stop(self):
        self.sp.pause_playback(device_id=self.device_id)

    def next(self):
        self.sp.next_track(self.device_id)
