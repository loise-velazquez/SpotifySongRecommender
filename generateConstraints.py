import sys
import spotipy
import spotipy.util as util
import pprint
import csv
import warnings
import random
import warnings

import connectSpotify

import pandas

def getRecommendedPlaylist(sp, classifier):
        song = connectSpotify.songSearch(sp)
        domain = recommendedSongs(sp, classifier)
        columns = song.shape[1]
        playLists = []

        for i in range(0, 10):
                attributes = []
                for j in range(0, 3):
                        index = random.randint(0, columns-1)
                        attributes.append([index, song.iloc[0, index], song.columns[index]])
                newPlayList = backTracking(song, domain, attributes)
                playLists.append(newPlayList)
        bestIndex = bestPlaylist(song, playLists, sp)
        theWinner = playLists[bestIndex]
        printPlayList(theWinner)
        
def printPlayList(playList):
        print("YOUR RECCOMMENDED PLAYLIST:")
        for i in range(0, len(playList)):
                songName = playList[i]['name']
                artist = playList[i]['artists'][0]['name']
                print(songName, "by", artist)
        print()

def bestPlaylist(song, playLists, sp):
        initialSongSum = songSum(song)
        bestPlayList = 0
        bestPlayListValue = 1000000000000000
        for i in range(0, len(playLists)):
                if playLists[i] is not None:
                        sumPlayList = 0
                        for j in range(0, len(playLists[i])):
                                songName = playLists[i][j]['name']
                                artist = playLists[i][j]['artists'][0]['name']
                                currSong = getAudioFeatures(songName, artist, sp)
                               
                                sumPlayList += songSum(currSong[0])
                        average = sumPlayList/len(playLists[i])
                        
                        if 1-abs(average/initialSongSum) < bestPlayListValue:
                                bestPlayListValue = 1 - abs(average/initialSongSum)
                                bestPlayList = i
        return bestPlayList
                        
def songSum(song):
        sumsong = 0
        for k in range(0, len(song.loc[0])):
                sumsong += song.loc[0][k]
        return sumsong

def backTracking(song, domain, attributes):
        playListLength = 5
        playList = []
        
        for i in range(0,len(domain[0])-1):
                if len(playList) >= 5:
                        return playList
                currentSong = domain[0][i]
                currentTrack = domain[1][i]
                if currentTrack not in playList:
                        if compareSongs(song, currentSong, attributes) is 1:
                                playList.append(currentTrack)

def compareSongs(song1, song2, attributes):
        warnings.filterwarnings("ignore")

        """
        print("song1")
        
        print(attributes[0][2])
        print(attributes[1][2])
        print(attributes[2][2])
        """
        
        at1 = abs(song1.loc[0][attributes[0][2]] / song2.loc[0][attributes[0][2]])
        at2 = abs(song1.loc[0][attributes[1][2]] / song2.loc[0][attributes[1][2]])
        at3 = abs(song1.loc[0][attributes[2][2]] / song2.loc[0][attributes[2][2]])

        total = (at1+at2+at3)/3
        if total < 2 and total > 0:
                return 1
        else:
                return 0


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
                songData = getAudioFeatures(songName, artist, sp)
                
                if (songData is not None):
                        prediction = classifier.predict(songData[0])[0]
                        if int(prediction) is 1:
                                songList.append(songData[0])
                                trackList.append(songData[1])
        return [songList, trackList]
        
def getAudioFeatures(name, artist, sp):
        results = sp.search(q=[name, artist], type="track", limit=1)

        items = results['tracks']['items']

        if (len(items) is not 0):
                track = items[0]
                features = sp.audio_features(track['id'])

                df = pandas.DataFrame(features)
                #song = df.drop(
                    #["uri", "track_href", "analysis_url", "id", "type", "duration_ms"], axis=1)
                df.to_csv('data/song.csv')
                
                song = pandas.read_csv('data/song.csv', usecols=lambda column: column not in
                        ["uri", "track_href", "analysis_url", "id", "type", "duration_ms"])
                return [song, track];
        return None
