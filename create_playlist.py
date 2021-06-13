import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl

from secrets import spotify_user_id, spotify_token


class CreatePlayList:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token,
        self.youtube_client = self.get_youtube_client()

    # Step 1: Log into YouTube
    def get_youtube_client(self):
        """ Log Into Youtube, Copied from Youtube Data API """
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    # Step 2: Grab liked videos
    def get_liked_videos(self):
        pass

    # Step 3: Create a New Playlist
    def create_playlist(self):
        request_body = json.dumps({
            "name": "Youtube Liked Vids",
            "description": "All Liked Youtube Videos",
            "public": True
        })

        query = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"

        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()

        # playlist id
        return response_json["id"]

    # Step 4: Search For the Song
    def get_spotify_uri(self, song_name, artist):
        query = f"https://api.spotify.com/v1/search?=track%3A{song_name}+artist%3A{artist}&type=track&offset=0&limit=20"

        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {spotify_token}"
            }
        )

        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # only use the first song
        uri = songs[0]["uri"]
        return uri

    # Step 5: Add this song into the new Spotify playlist
    def add_song_to_playlist(self):
        pass
