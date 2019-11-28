import psycopg2
from playlist_gen.config import HOST, DATABASE, USER, PASSWORD, SCHEMA


class Playlist:
    def __init__(self, name, date, songs):
        self.name = name
        self.date = date
        self.songs = songs

    def addSongs(self, playlist_id):
        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        except ConnectionError:
            print("error connecting to database when adding songs")
            return False
        cur = conn.cursor()
        try:
            for song in self.songs:
                # check if exists
                sql = "SELECT EXISTS(SELECT 1 FROM dg_schema.tracks WHERE tracks.artist_name= %s AND " \
                    "tracks.song_name= %s); "
                cur.execute(sql, (song.artist, song.name))
                if cur.fetchone()[0]:
                    sql = "SELECT dg_schema.tracks.track_id FROM dg_schema.tracks WHERE tracks.artist_name= %s AND " \
                          "tracks.song_name= %s; "
                    cur.execute(sql, (song.artist, song.name))
                else:
                    sql = "INSERT INTO dg_schema.tracks (artist_name, song_name) "
                    sql += "VALUES (%s, %s) RETURNING track_id;"
                    cur.execute(sql, (song.artist, song.name))
                    conn.commit()

                song_id = cur.fetchone()[0]

                # make sure this entry doesnt already exist (superfluous once we exit if playlist already exist)
                sql = "SELECT EXISTS(SELECT 1 FROM dg_schema.playlist_tracks WHERE playlist_tracks.playlist_id= %s " \
                      "AND playlist_tracks.track_id= %s); "
                cur.execute(sql, (playlist_id, song_id))
                if not cur.fetchone()[0]:
                    # add into playlist_tracks now
                    sql = "INSERT INTO dg_schema.playlist_tracks (playlist_id, track_id, track_position, " \
                          "track_request) "
                    sql += "VALUES (%s, %s, %s, %s);"
                    cur.execute(sql, (playlist_id, song_id, song.position, song.request))
                    conn.commit()

            return True
        except psycopg2.DataError:
            print("invalid sql")
            return False
        finally:
            conn.close()

    def addPlaylist(self):
        # add songs first
        # success = self.addSongs(self.songs)
        # open connection
        try:
            conn = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        except ConnectionError:
            print("Error, unable to connect to database")
            return 0

        cur = conn.cursor()
        try:
            # check if exists
            sql = "SELECT EXISTS(SELECT 1 FROM dg_schema.playlist WHERE playlist.playlist_name = '" + self.name + "'); "
            cur.execute(sql)
            if cur.fetchone()[0]:
                sql = "SELECT dg_schema.playlist.playlist_id FROM dg_schema.playlist WHERE " \
                  "playlist.playlist_name = '" + self.name + "'; "
                cur.execute(sql)
                return cur.fetchone()[0]

            sql = "INSERT INTO dg_schema.playlist (playlist_name, playlist_date, playlist_spotify) "
            sql += "VALUES (%s, %s, %s) RETURNING playlist_id;"
            cur.execute(sql, (self.name, self.date, False))
            conn.commit()
            return cur.fetchone()[0]
        except psycopg2.DataError:
            print("sql statement was invalid")
            return 0
        finally:
            conn.close()


class Song:
    def __init__(self, artist, name, position, request):
        self.name = name
        self.artist = artist
        self.position = position
        self.request = request
