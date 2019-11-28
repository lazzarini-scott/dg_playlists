from playlist_gen.scraper.scraper import Scraper
from Database import DatabaseConnection
import sys
import psycopg2
from playlist_gen.config import ENABLE_DATABASE

def run():
    # command line arguments here. include check for arguments, if they don't exist then just run normally,
    # if one equals "historic" then use historic
    all_playlists = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            all_playlists = True
    scraper = Scraper()
    playlists = scraper.scrape_playlist_data(all_playlists)
    # interact with database
    for playlist in playlists:
        playlist_id = playlist.addPlaylist()
        if playlist_id == 0:
            print("Error with adding playlist to database!")
            return
        success = playlist.addSongs(playlist_id)
        # success.addtospotify()


