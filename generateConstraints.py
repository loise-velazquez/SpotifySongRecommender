import sys
import spotipy
import spotipy.util as util
import pprint
import csv
import warnings
import random

import connectSpotify

import pandas

def getRecommendedPlaylist(sp, classifier):
        song = connectSpotify.songSearch(sp)
        domain = recommendedSongs(sp, classifier)
        columns = song.shape[1]
        playLists = []

        print(song)

        for i in range(0, 10):
                attributes = []
                for j in range(0, 3):
                        index = random.randint(0, columns-1)
                        attributes.append([index, song.iloc[0, index], song.columns[index]])
                newPlayList = backTracking(song, domain, attributes)

def backTracking(song, domain, attributes):
        playListLength = 5
        playList = []
        
        for i in range(0,len(domain[0])-1):
                if len(playList) >= 5:
                        return playList
                currentSong = domain[0][i]
                currentTrack = domain[1][i]
                if currentSong not in playList:
                        if compareSongs(song, currentSong, attributes) is 1:
                                playList.append(currentTrack)
        return playList;

def compareSongs(song1, song2, attributes):
        print("song1")
        """
        print(attributes[0][2])
        print(attributes[1][2])
        print(attributes[2][2])
        """
        
        at1 = abs(song1.loc[0][attributes[0][2]] / song2.loc[0][attributes[0][2]])
        at2 = abs(song1.loc[0][attributes[1][2]] / song2.loc[0][attributes[1][2]])
        at3 = abs(song1.loc[0][attributes[2][2]] / song2.loc[0][attributes[2][2]])

        total = (at1+at2+at3)/3
        print(total)


def recommendedSongs(sp, classifier):
        data = pandas.read_csv(
            'data/data.csv', usecols=lambda column: column in ["song_title", "artist"])
        rows = data.shape[0]
        songList = []
        trackList = []
        
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
                                songList.append(song)
                                trackList.append(track)
        return [songList, trackList]
        
        
