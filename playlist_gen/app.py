from playlist_gen.scraper.scraper import Scraper
import sys
from playlist_gen.config import HISTORIC_URL, PLAYLIST_URL

def main():
    # command line arguments here. include check for arguments, if they don't exist then just run normally,
    # if one equals "historic" then use historic
    all_playlists = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            all_playlists = True

    scraper = Scraper()
    scraper.scrape_playlist_data(all_playlists)
    playlists = scraper.playlists