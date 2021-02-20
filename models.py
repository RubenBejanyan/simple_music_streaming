from uuid import uuid3, NAMESPACE_DNS
from datetime import date
import json


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


class MediaObject:
    def __init__(self):
        self.path = f'./data/{type(self).__name__}.txt'

    def save(self):
        object_info = {k: v for k, v in self.__dict__.items() if k != 'path'}
        with open(self.path, 'r') as my_f:
            my_data = [json.loads(line) for line in my_f.readlines()]
        if object_info in my_data:
            return
        with open(self.path, 'a+') as mf:
            mf.write(f'{json.dumps(object_info)}\n')

    def update(self, **kwargs):
        exist = set(self.__dict__.keys())
        print(f'in update dict{self.__dict__}')
        not_match = {key for key in kwargs.keys() if key not in exist}
        if not_match:
            raise Exception(f"{type(self).__name__} doesn't have {not_match} fields! Use fields from {exist}")
        for key in kwargs.keys():
            if kwargs[key] != getattr(self, key):
                self.delete()
                setattr(self, key, kwargs[key])
                self.save()

    def delete(self):
        object_info_json = json.dumps({k: v for k, v in self.__dict__.items() if k != 'path'})
        with open(self.path, 'r') as my_f:
            lines = my_f.readlines()
        print(object_info_json, '\n', lines)
        if f'{object_info_json}\n' in lines:
            with open(self.path, 'w') as new_f:
                for line in lines:
                    if line.strip('\n') != object_info_json:
                        new_f.write(line)
        else:
            raise Exception(f'No {type(self).__name__} object founded')

    @classmethod
    def filter(cls, **kwargs):
        class_path = f'./data/{cls.__name__}.txt'
        filtering_attributes = set(kwargs.keys())
        filtering_values = list(kwargs.values())
        with open(class_path, 'r') as my_f:
            my_data = [json.loads(line) for line in my_f.readlines()]
        result = []
        if any(item not in my_data[0].keys() for item in filtering_attributes):
            raise Exception(f'something from {filtering_attributes} not {cls.__name__} attribute')
        for my_object in my_data:
            if all(item in my_object.values() for item in filtering_values):
                my_object.pop('id')
                result.append(cls(**my_object))
        return result

    @classmethod
    def get(cls, **kwargs):
        class_path = f'./data/{cls.__name__}.txt'
        getting_attributes = set(kwargs.keys())
        getting_values = list(kwargs.values())
        with open(class_path, 'r') as my_f:
            my_data = [json.loads(line) for line in my_f.readlines()]
        if any(item not in my_data[0].keys() for item in getting_attributes):
            raise Exception(f'something from {getting_attributes} not {cls.__name__} attribute')
        already_match = False
        result = None
        for my_object in my_data:
            if all(item in my_object.values() for item in getting_values):
                if not already_match:
                    my_object.pop('id')
                    result = cls(**my_object)
                    already_match = True
                else:
                    raise Exception(f'Multiple {cls.__name__} objects founded')
        if result:
            return result
        else:
            raise Exception(f'No {cls.__name__} objects founded')


class User(MediaObject):

    def __init__(self, first_name, last_name, email, password,
                 profile_picture=None, birth_date=None, level=0, song_playing=None):
        super(User, self).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.profile_picture = profile_picture
        self.birth_date = birth_date
        self.level = level
        self.id = uuid3(NAMESPACE_DNS, str(self.email)).hex
        self.song_playing = song_playing

    def validate_user(self):
        if self.first_name is None or self.last_name is None:
            return False
        elif not valid_email(self.email):
            return False
        elif not valid_password(self.password):
            return False
        return True

    def create_playlist(self, name):
        new_playlist = Playlist(name=name, created_by=self.id)
        return new_playlist

    def delete_playlist(self, name):
        Playlist.get(name=name, created_by=self.id).delete()


class Artist(User):
    def __init__(self, first_name, last_name, email, password,
                 profile_picture=None, birth_date=None, level=0, about=None, song_playing=None, listeners_count=0):
        super(Artist, self).__init__(first_name=first_name, last_name=last_name, email=email,
                                     password=password, profile_picture=profile_picture, birth_date=birth_date,
                                     level=level, song_playing=song_playing)
        self.about = about
        self.listeners_count = listeners_count

    # in task file, but it not enough to create song, or in file must be info about duration, genre, year, album
    def add_song(self, title: str, artist_name: str, duration, genre, year, album=None):
        new_song = Song(title=title, artist=artist_name, duration=duration, genre=genre,
                        year=year, created_by=self.id, album=album)
        return new_song

    def delete_song(self, song_id):
        song_to_delete = Song.get(id=song_id, created_by=self.id)
        song_to_delete.delete()

    def create_album(self, title, label, year, list_of_song_url=None, picture_url=None):
        new_album = Album(label=label, year=year, name=title, created_by=self.id,
                          picture_url=picture_url, song_list=list_of_song_url)
        return new_album


class Song(MediaObject):
    def __init__(self, title, artist, duration, genre, year, created_by, album=None, streams_count=0):
        super(Song, self).__init__()
        self.title = title
        self.artist = artist
        self.duration = duration
        self.genre = genre
        self.year = year
        self.created_by = created_by
        self.streams_count = streams_count
        self.id = uuid3(NAMESPACE_DNS, f'{self.created_by}{self.title}').hex
        if not album:
            album = Album(label=None, year=self.year, name=self.title, created_by=self.created_by, song_list=[self.id])
            album.save()
            album = album.id
        self.album = album

    def validate(self):
        # did not need, because if we have not artist with that id, get method raise exception
        if not Artist.get(id=self.created_by):
            raise Exception('Access denied')

    def add_to_playlist(self, playlist, user: User):
        playlist_to_add = Playlist.get(id=playlist, created_by=user.id)
        song_list = list(playlist.song_list)
        if song_list:
            playlist.song_list = tuple(song_list.append(self.id))
        else:
            playlist.song_list = (self.id)
        playlist.save()
        print('updated')

    def remove_from_playlist(self, playlist, user):
        users_playlist = Playlist.get(name=playlist, created_by=user.id)
        if self.id in users_playlist.song_list:
            users_playlist.song_list.remove(self.id)
            users_playlist.update(song_list=users_playlist.song_list)
        else:
            raise Exception(f'No {self.title} in playlist:{users_playlist.id}')

    def play(self, user, start_time=0):
        if user.song_playing:
            users_splays = SongPlays.get(id=user.song_playing)
            users_splays.stop_the_song()
        playing_song = SongPlays(user=user.id, song=self.id, start_timestamp=start_time)
        self.update(streams_count=self.streams_count + 1)
        artist = Artist.get(id=self.created_by)
        artist.update(listeners_count=artist.listeners_count + 1)
        playing_song.save()
        return playing_song.playing()

    def stop(self, user):
        playing_song = SongPlays(user=user.id, song=self.id)
        users_splay = SongPlays.get(id=user.song_playing)
        if users_splay.song != self:
            raise Exception(f'{self.title} not play for user: {user.id} now')
        playing_song.stop_the_song()

    def download(self):
        return self.path


class Playlist(MediaObject):
    def __init__(self, name, created_by, date_added=None, picture_url=None, song_list=[]):
        super(Playlist, self).__init__()
        self.name = name
        if date_added is None:
            date_added = str(date.today())
        self.date_added = date_added
        self.created_by = created_by
        self.picture_url = picture_url
        if song_list:
            song_list = tuple(song_list)
        self.song_list = song_list
        self.id = uuid3(NAMESPACE_DNS, f'{self.created_by}{self.name}').hex

    def play(self):
        user = User.get(id=self.created_by)
        for song_id in self.song_list:
            print('song id', song_id)
            song = Song.get(id=song_id)
            song.play(user=user)

    def stop(self):
        user = User.get(id=self.created_by)
        user.song_playing.stop_the_song()


class Album(Playlist):
    def __init__(self, label, year, name, created_by, picture_url=None, song_list=None):
        super(Album, self).__init__(name=name, created_by=created_by, picture_url=picture_url, song_list=song_list)
        self.label = label
        self.year = year

    def validate(self):
        if not Artist.get(id=self.created_by):
            raise Exception('Access denied')


class SongPlays(MediaObject):
    def __init__(self, user, song, start_timestamp=0):
        super(SongPlays, self).__init__()
        self.user = user
        self.song = song
        self.start_timestamp = start_timestamp
        self.id = uuid3(NAMESPACE_DNS, f'{self.user}{self.song}').hex

    def playing(self):
        song = Song.get(id=self.song)
        my_user = User.get(id=self.user)
        play_time = song.duration - self.start_timestamp
        my_user.song_playing = self.id
        my_user.update(song_playing=self.id)
        self.save()
        print(f'song "{song.title}" play for user:{self.user} for {play_time} seconds')

    def stop_the_song(self):
        self.user.song_playing = None
        self.user.update(song_playing=None)
        self.delete()


class PlaylistSong:
    def __init__(self, playlist, song, date_added):
        self.playlist = playlist
        self.song = song
        self.date_added = date_added


if __name__ == '__main__':
    bobby = User('Bob', 'Marley', 'bob@com', '7414tUn&')
    bobby.save()
    bobby.update(first_name='jan')
    my_song = Song.get(title='wonderful world')
    new_playlist = bobby.create_playlist('other6')
    new_playlist.save()
    my_song.add_to_playlist(new_playlist, bobby)
    new_playlist.play()
    print(new_playlist.song_list)
