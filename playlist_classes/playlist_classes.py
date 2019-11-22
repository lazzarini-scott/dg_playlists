class Playlist:
    def __init__(self, name, date, songs):
        self.name = name
        self.date = date
        self.songs = songs

class Song:
    def __init__(self, artist, name, position):
        self.name = name
        self.artist = artist
        self.position = position