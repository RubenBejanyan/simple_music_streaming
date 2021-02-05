import uuid


class User:

    def __init__(self, first_name, last_name, email, password, profile_picture=None, birth_date=None, level=0):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.profile_picture = profile_picture
        self.birth_date = birth_date
        self.level = level
        self.id = uuid.uuid3()  # search what i need give to that function as parameter

    def validate_user(self):
        pass

    def create_playlist(self, name):
        pass

    def delete_playlist(self, name):
        pass


class Artist(User):
    def __init__(self, about=None, listeners_count=0):
        self.about = about
        self.listeners_count = listeners_count

    def add_song(self, title: str, artist_name: str, file: str):
        pass

    def delete_song(self, song_id):
        pass

    def create_album(self, title, label, year, list_of_song_url=[]):
        pass


class Song:
    def __init__(self, title: str, artist: str, duration: int, genre: str,
                 year: int, created_by, album, streams_count=0):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.genre = genre
        self.year = year
        self.created_by = created_by
        self.streams_count = streams_count
        self.album = album

    def validate(self):
        pass

    def add_to_playlist(self, playlist, user):
        pass

    def remove_from_playlist(self, playlist, user):
        pass

    def play(self, user):
        pass

    def stop(self, user):
        pass

    def download(self):
        pass


class Playlist:
    def __init__(self, name, date_added, created_by, picture_url):
        self.name = name
        self.date_added = date_added  # may be need to add date automatically
        self.created_by = created_by
        self.picture_url = picture_url

    def play(self):
        pass

    def stop(self):
        pass


class Album(Playlist):
    def __init__(self, label, year):
        self.label = label
        self.year = year

    def validate(self):
        pass


class SongPlayes:
    def __init__(self, user, song, start_timestamp):
        self.user = user
        self.song = song
        self.start_timestamp = start_timestamp


class PlaylistSong:
    def __init__(self, playlist, song, date_added):
        self.playlist = playlist
        self.song = song
        self.date_added = date_added
