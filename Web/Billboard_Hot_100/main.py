from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests, os, spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

load_dotenv()

billboard_url = 'https://www.billboard.com/charts/hot-100'

date_str = input('Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n')
response = requests.get(f'{billboard_url}/{date_str}')
response.raise_for_status()

year = date_str.split('-')[0]

soup = BeautifulSoup(response.text, 'html.parser')
tags = soup.select('li h3#title-of-a-story')
titles = [tag.getText().strip() for tag in tags]
tags = soup.select('li h3#title-of-a-story + span')
artists = [tag.getText().strip() for tag in tags]

title_artists = list(zip(titles, artists))

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SPOTIFY_USER = os.getenv('SPOTIFY_USER')
# auth_manager = SpotifyClientCredentials()

auth_manager = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, 
                            client_secret=SPOTIFY_CLIENT_SECRET, 
                            redirect_uri=SPOTIFY_REDIRECT_URI, 
                            state=None, 
                            scope='playlist-modify-public', 
                            cache_path=None, 
                            # username='manch', 
                            username=SPOTIFY_USER,
                            proxies=None, 
                            show_dialog=False, 
                            requests_session=True, 
                            requests_timeout=None)

sp = spotipy.Spotify(auth_manager=auth_manager)

tracks = []
for title, artist in title_artists:
    # results = sp.search(q=f'{title} artist:{artist}', type='track')
    
    results = sp.search(q=f'{title} artist:{artist}', type='track')
    if len(results['tracks']['items']) > 0:
        item = results['tracks']['items'][0]
    else:
        results = sp.search(q=f'{title}', type='track')
        if len(results['tracks']['items']) > 0:
            item = results['tracks']['items'][0]
        else:
            continue
    
    uri = item['uri']
    url = item['external_urls']['spotify']
    result_title = item['name']
    result_artist = item['artists'][0]['name']
    # print(f'title:{title}  result_title:{result_title}  artist:{artist} result_artist:{result_artist}  url:{url}  uri:{uri}')
    tracks.append(uri)


playlist_id = sp.user_playlist_create(SPOTIFY_USER, f'{date_str} Billboard 100')
# print(f'playlist_id: {playlist_id}')
if playlist_id is not None:
    sp.user_playlist_add_tracks(SPOTIFY_USER, playlist_id['id'], tracks)
