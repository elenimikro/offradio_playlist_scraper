'''
Created on 24 Nov 2013

@author: elenimikroyannidi
'''
from bs4 import BeautifulSoup
from urllib2 import urlopen
import spotify.manager
import getpass

BASE_URL = "http://www.offradio.gr/player/#tabs-2"

class SessionManager(spotify.manager.SpotifySessionManager):
    def logged_in(self, session, error):
        print "User", session.display_name(), "has been logged in"
#         session.search("ABBA", self.results_loaded, 
#                        track_offset=0, track_count=5, album_offset=0, album_count=5, 
#                        artist_offset=0, artist_count=5)
        
    def results_loaded(self, results, userdata):
#         print results.total_albums(), "album results in total"
#         print "First", len(results.albums()), "albums:"
#         for album in results.albums():
#             print album.name()
        
        print results.total_tracks(), "track results in total"
        print "First", len(results.tracks()), "tracks:"
        for track in results.tracks():
            print track.name()
    
    def search_list(self, session, spotify_queries):
        print '\n'
        for song in spotify_queries:
            print song
            self.session.search(song, self.results_loaded, track_offset=0, track_count=1)
#         spotify.Link.from_string(song)
#         trackList = spotify.Results.tracks(song)
#         for track in trackList:
#             print track

def search_spotify(spotify_queries):
    print "Please enter your Spotify password"
    pw = getpass.getpass()
    sess = SessionManager("mikrohelen", pw)
    session = sess.connect()
    sess.search_list(spotify_queries, session)
    sess.disconnect()
    


def get_song_list():
    spotify_queries = set()
    html = urlopen(BASE_URL).read()
    soup = BeautifulSoup(html, "lxml")
#     soup.prettify('utf-8')
    
#   class="view-content"  
#     for field in soup.find_all("div","views-field views-field-title"):
#     for field in soup.find_all("span", "field-content"):

    playlist_tab = soup.find('div', attrs={"id":"tabs-2"})
    links = soup.find_all('a', attrs={"class":"llastfm"})
#     print playlist_tab
    links = playlist_tab.findAll('a')
    for link in links:
        print link.encode('utf-8')
    print links
    empty_songs = [s.getText().strip() for s in playlist_tab.findAll('div')]
#     links = empty_songs.findAll('div', attrs={"id":"hidden-links"})
#     print links
    songs = empty_songs[0].splitlines()
#     print songs
    id=1
    for song in songs:
        if song.strip() and song.find('LASTFM') and song.find('ITUNES') and song.find('AMAZON') and song.find('GOOGLE') and song.find('OFFRADIO PLAYLIST'):
            song2 = str(song.encode('utf-8'))
            if len(song2)>10:
                spotify_query = str(song.encode('utf-8'))
                print str(id) + '. ' + spotify_query
                id+=1
                spotify_queries.add(spotify_query)
    search_spotify(spotify_queries)
    

if __name__ == '__main__':
    get_song_list()