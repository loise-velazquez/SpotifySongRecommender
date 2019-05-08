import sys
import spotipy
import spotipy.util as util
import pprint
import csv
import warnings

from connectSpotify import nueralNetwork

import pandas

def readData(classifier):
    data = pandas.read_csv('data/song.csv', usecols = lambda column : column not in 
            ["uri" , "track_href", "analysis_url", "id", "type", "duration_ms"])

    # put songs into some sort of a list

    #use spotipy to search for all of the songs

    # feed results int odecision tree or neural network

    #if song prediction = 1, add that song to our lost of songs the user likes 

    #next do constraint satisfaction stuff 
