import requests
import textile
import datetime
from bs4 import BeautifulSoup
from playlist_classes.playlist_classes import Playlist, Song
from playlist_gen.config import HISTORIC_URL, PLAYLIST_URL

class Scraper:
    def __init__(self):
        self.playlists = []

    def get_playlist(self, url):
        r = requests.get(url)
        html = textile.textile(r.text)
        soup = BeautifulSoup(html, features="html5lib")
        playlist_raw_text = soup.find(id="playlist")
        playlist_raw_list = playlist_raw_text.get_text().splitlines()
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November",
                  "December"]
        date = ""
        main_room = []
        for line in playlist_raw_list:
            if line == "Lounge":
                break
            if date == "":
                for month in months:
                    if month in line:
                        date = line
            else:
                if (" – " in line):
                    main_room.append(line)

        return date, main_room

    def get_all_playlist_links(self, url):
        r = requests.get(url)
        html = textile.textile(r.text)
        soup = BeautifulSoup(html, features="html5lib")
        links = []
        url_header = "http://www.deathguild.com/"

        for a in soup.find_all('a', href=True):
            if "/playlist/" in a['href']:
                links.append(url_header + a['href'])

        return links

    def add_playlist(self, playlist):
        # TODO - adds playlist info to database if config says so
        pass

    def organize_playlist_data(self, date, playlist):
        position = 1
        song_objs = []
        for track in playlist:
            song_data = track.rsplit(' – ', 1)
            song_name = song_data[1]
            isRequest = False
            if(song_name.endswith('R')):
                isRequest = True
                song_name = song_name[:-1]
            song_objs.append(Song(song_data[0], song_name, position, isRequest))
            position += 1

        date_time = datetime.datetime.strptime(date.split('\t')[1], "%B %d, %Y")
        return Playlist("Death Guild - " + str(date_time.date()) + " - Main", date_time.date(), song_objs)

    def scrape_playlist_data(self, all_playlists):
        links = []
        playlist_objs = []
        if(all_playlists):
            links = self.get_all_playlist_links(HISTORIC_URL)
        else:
            links.append(PLAYLIST_URL)

        for link in links:
            date, playlist_raw = self.get_playlist(link)
            playlist_obj = self.organize_playlist_data(date, playlist_raw)
            # add here?
            playlist_objs.append(playlist_obj)

        return playlist_objs

