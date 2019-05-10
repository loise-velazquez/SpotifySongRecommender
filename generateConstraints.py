import sys
import spotipy
import spotipy.util as util
import pprint
import csv
import warnings
import random

import pandas

    #use spotipy to search for all of the songs

    # feed results int odecision tree or neural network

    #if song prediction = 1, add that song to our lost of songs the user likes 

    #next do constraint satisfaction stuff

def recommendedSongs(sp, classifier):
        data = pandas.read_csv(
            'data/data.csv', usecols=lambda column: column in ["song_title", "artist"])
        rows = data.shape[0]
        songList = []
        
        
        for counter in range(0,50):
                i = random.randint(0, rows-1)
                songName = data.loc[i]['song_title']
                artist = data.loc[i]['artist']
                results = sp.search(q=[songName, artist], type="track", limit=1)

                items = results['tracks']['items']
                
                if (len(items) is not 0):
                        track = items[0]
                        features = sp.audio_features(track['id'])
                        
                        df = pandas.DataFrame(features)
                        
                        df.to_csv('data/song.csv')
                        song = pandas.read_csv('data/song.csv', usecols=lambda column: column not in
                                        ["uri", "track_href", "analysis_url", "id", "type", "duration_ms"])
                        
                        prediction = classifier.predict(song)[0]
                        if int(prediction) is 1:
                                songList.append(track)
        return songList
        
        
