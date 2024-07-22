import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time


# Retrieve Spotify API credentials from environment variables
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
scope = 'playlist-modify-public playlist-modify-private playlist-read-private'

# Ensure credentials are loaded
if not all([client_id, client_secret, redirect_uri]):
    raise ValueError("Spotify API credentials are not set in environment variables.")

# Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# User ID
user_id = sp.current_user()['id']

# Playlist name and new combined playlist name
existing_playlist_name = '🌌 The Sixth Lane 🌌'
playlist_names = [
    '🌌 The First Lane 🌌',
    '🌌 The Second Lane 🌌',
    '🌌 The Third Lane 🌌',
    '🌌 The Fourth Lane 🌌',
    '🌌 The Fifth Lane 🌌',
    '🌌 The Sixth Lane 🌌',
    '🌌 The Seventh Lane 🌌',
    '🌌 The Eighth Lane 🌌',
    '🌌 The Ninth Lane 🌌',
    '🌌 The Tenth Lane 🌌'
]

# Get all playlists
playlists = sp.current_user_playlists()
existing_playlist_id = None
playlist_ids = {}

# Find the existing playlist and other playlists
for playlist in playlists['items']:
    if playlist['name'] == existing_playlist_name:
        existing_playlist_id = playlist['id']
    elif playlist['name'] in playlist_names:
        playlist_ids[playlist['name']] = playlist['id']

if not existing_playlist_id:
    print(f"Playlist '{existing_playlist_name}' not found.")
    exit()

# Remove all tracks from the existing playlist
def remove_all_tracks_from_playlist(playlist_id):
    while True:
        # Fetch the tracks from the playlist
        tracks = sp.playlist_tracks(playlist_id)
        track_ids = [item['track']['id'] for item in tracks['items']]
        
        # If there are no tracks left, exit the loop
        if not track_ids:
            break
        
        # Remove tracks in batches of 100
        for i in range(0, len(track_ids), 100):
            sp.playlist_remove_all_occurrences_of_items(playlist_id, track_ids[i:i+100])
            time.sleep(1)  # Introduce a delay to handle rate limits

    print(f'All tracks removed from "{existing_playlist_name}".')

print(f'Removing all tracks from "{existing_playlist_name}"...')
remove_all_tracks_from_playlist(existing_playlist_id)

# Collect tracks from playlists in order
tracks = []
for name in playlist_names:  # Process playlists in the given order
    if name in playlist_ids:
        pid = playlist_ids[name]
        results = sp.playlist_tracks(pid)
        tracks.extend([item['track']['uri'] for item in results['items']])

# Add tracks to the existing playlist in chunks of 100 (Spotify API limit)
print(f'Adding tracks to "{existing_playlist_name}"...')
for i in range(0, len(tracks), 100):
    sp.playlist_add_items(existing_playlist_id, tracks[i:i+100])
    time.sleep(1)  # Introduce a delay to handle rate limits

print(f'All tracks added to "{existing_playlist_name}".')