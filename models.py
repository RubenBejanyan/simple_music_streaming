import uuid


def valid_email(email):
    if '@' in email:
        return True
    return False


def valid_password(password):
    length = False
    uppercase = False
    lowercase = False
    number = False
    special_char = False
    if len(password) >= 8:
        length = True
    for character in password:
        if character.isupper():
            uppercase = True
        elif character.islower():
            lowercase = True
        elif not character.isalnum():
            special_char = True
        elif character.isnumeric():
            number = True
    return length and uppercase and lowercase and special_char and number


class User:

    def __init__(self, first_name, last_name, email, password, profile_picture=None, birth_date=None, level=0):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.profile_picture = profile_picture
        self.birth_date = birth_date
        self.level = level
        self.id = uuid.uuid3(uuid.NAMESPACE_DNS, str(self.last_name))

    def validate_user(self):
        if self.first_name is None or self.last_name is None:
            return False
        elif not valid_email(self.email):
            return False
        elif not valid_password(self.password):
            return False
        return True

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


class SongPlays:
    def __init__(self, user, song, start_timestamp):
        self.user = user
        self.song = song
        self.start_timestamp = start_timestamp


class PlaylistSong:
    def __init__(self, playlist, song, date_added):
        self.playlist = playlist
        self.song = song
        self.date_added = date_added


