import sys
import spotipy
import spotipy.util as util
import pprint
import csv
import warnings
import pandas
import random


#Graph Structure for searching for songs


def create_like_songs():
    """Collects songs and creates an adjacency list based on user
        selected song characteristic and groups like songs together"""
    data = pandas.read_csv(
        'data/data.csv', usecols=lambda column: column in ["acousticness", "energy", "loudness", "tempo", "song_title", "artist"] )
    rows = data.shape[0]
    choice = input("Please select a song characteristic to generate the structure by. You may choose: acousticness, energy, loudness, or tempo. ")

    adjList = [[],[],[],[],[],[],[],[],[],[]]
    smallBoundary = 1.0/10
    loudBoundary = 5.0 
    tempoBoundary = 20.0
    if choice.lower() == "acousticness":
        print ("You chose acoustic!")
        
        for i in range(rows):
            if float(data.loc[i]['acousticness']) < smallBoundary:
                adjList[0].append(data.loc[i])
            elif float(data.loc[i]['acousticness']) < smallBoundary*2:
                adjList[1].append(data.loc[i])
            elif float(data.loc[i]['acousticness']) < smallBoundary*3:
                adjList[2].append(data.loc[i])
            elif float(data.loc[i]['acousticness']) < smallBoundary*4:
                adjList[3].append(data.loc[i])
            elif float(data.loc[i]['acousticness']) < smallBoundary*5:
                adjList[4].append(data.loc[i])
            elif float(data.loc[i]['acousticness']) < smallBoundary*6:
                adjList[5].append(data.loc[i])
            elif float(data.loc[i]['acousticness']) < smallBoundary*7:
                adjList[6].append(data.loc[i])
            elif float(data.loc[i]['acousticness']) <smallBoundary*8:
                adjList[7].append(data.loc[i])
            elif float(data.loc[i]['acousticness']) <smallBoundary*9:
                adjList[8].append(data.loc[i])
            else:
                adjList[9].append(data.loc[i])
    elif choice.lower() == "energy":
        print ("You chose energy!")
        for i in range(rows):
            if float(data.loc[i]['energy']) <smallBoundary:
                adjList[0].append(data.loc[i])
            elif float(data.loc[i]['energy']) <smallBoundary*2:
                adjList[1].append(data.loc[i])
            elif float(data.loc[i]['energy']) <smallBoundary*3:
                adjList[2].append(data.loc[i])
            elif float(data.loc[i]['energy']) <smallBoundary*4:
                adjList[3].append(data.loc[i])
            elif float(data.loc[i]['energy']) <smallBoundary*5:
                adjList[4].append(data.loc[i])
            elif float(data.loc[i]['energy']) <smallBoundary*6:
                adjList[5].append(data.loc[i])
            elif float(data.loc[i]['energy']) <smallBoundary*7:
                adjList[6].append(data.loc[i])
            elif float(data.loc[i]['energy']) <smallBoundary*8:
                adjList[7].append(data.loc[i])
            elif float(data.loc[i]['energy']) <smallBoundary*9:
                adjList[8].append(data.loc[i])
            else:
                adjList[9].append(data.loc[i])
    elif choice.lower() == "loudness":
        print ("You chose loudness!")
        for i in range(rows):
            #print(data.loc[i]['loudness'])
            if abs(float(data.loc[i]['loudness'])) <loudBoundary*9:
                adjList[0].append(data.loc[i])
            elif abs(float(data.loc[i]['loudness'])) <loudBoundary*8:
                adjList[1].append(data.loc[i])
            elif abs(float(data.loc[i]['loudness'])) <loudBoundary*7:
                adjList[2].append(data.loc[i])
            elif abs(float(data.loc[i]['loudness'])) <loudBoundary*6:
                adjList[3].append(data.loc[i])
            elif abs(float(data.loc[i]['loudness'])) <loudBoundary*5:
                adjList[4].append(data.loc[i])
            elif abs(float(data.loc[i]['loudness'])) <loudBoundary*4:
                adjList[5].append(data.loc[i])
            elif abs(float(data.loc[i]['loudness'])) <loudBoundary*3:
                adjList[6].append(data.loc[i])
            elif abs(float(data.loc[i]['loudness'])) <loudBoundary*2:
                adjList[7].append(data.loc[i])
            elif abs(float(data.loc[i]['loudness'])) <loudBoundary*1:
                adjList[8].append(data.loc[i])
            else:
                adjList[9].append(data.loc[i])
    elif choice.lower() == "tempo":
        print ("You chose tempo!")
        for i in range(rows):
            if float(data.loc[i]['tempo']) <tempoBoundary:
                adjList[0].append(data.loc[i])
            elif float(data.loc[i]['tempo']) <tempoBoundary*2:
                adjList[1].append(data.loc[i])
            elif float(data.loc[i]['tempo']) <tempoBoundary*3:
                adjList[2].append(data.loc[i])
            elif float(data.loc[i]['tempo']) <tempoBoundary*4:
                adjList[3].append(data.loc[i])
            elif float(data.loc[i]['tempo']) <tempoBoundary*5:
                adjList[4].append(data.loc[i])
            elif float(data.loc[i]['tempo']) <tempoBoundary*6:
                adjList[5].append(data.loc[i])
            elif float(data.loc[i]['tempo']) <tempoBoundary*7:
                adjList[6].append(data.loc[i])
            elif float(data.loc[i]['tempo']) <tempoBoundary*8:
                adjList[7].append(data.loc[i])
            elif float(data.loc[i]['tempo']) <tempoBoundary*9:
                adjList[8].append(data.loc[i])
            else:
                adjList[9].append(data.loc[i])
    else:
        print ("Please select a valid characteristic")

    return adjList

def characteristic_intensity(adjList):
    """This function asks user to specify how much they want 
        their playlist to be representative of the characteristic chosen"""
    intensity = input("On a scale of 1-10 how much of that characteristic do you want? ")
    intensity = int(intensity)
    print ("You chose " + str(intensity))
    if intensity == 1:
        list = adjList[0]
    elif intensity == 2:
        list = adjList[1]
    elif intensity == 3:
        list = adjList[2]
    elif intensity == 4:
        list = adjList[3]
    elif intensity == 5:
        list = adjList[4]
    elif intensity == 6:
        list = adjList[5]
    elif intensity == 7:
        list = adjList[6]
    elif intensity == 8:
        list = adjList[7]
    elif intensity == 9:
        list = adjList[8]
    elif intensity == 10:
        list = adjList[9]
    else:
        print("Please choose a valid intensity.")
    
    print ("There are " + str(len(list)) + " songs that fit your preferences!")
    return list

def narrow_down(list):
    """Function takes result from intensity then narrows down again
       using a second characteristic. Does not discriminate if same one"""
    choice = input("Please select another song characteristic to help focus your playlist. ")

    adjList = [[],[],[],[],[],[],[],[],[],[]]
    smallBoundary = 1.0/10
    loudBoundary = 5.0 
    tempoBoundary = 20.0
    if choice.lower() == "acousticness":
        print ("You chose acoustic!")
        
        for i in range(len(list)):
            if float(list[i]['acousticness']) < smallBoundary:
                adjList[0].append(list[i])
            elif float(list[i]['acousticness']) < smallBoundary*2:
                adjList[1].append(list[i])
            elif float(list[i]['acousticness']) < smallBoundary*3:
                adjList[2].append(list[i])
            elif float(list[i]['acousticness']) < smallBoundary*4:
                adjList[3].append(list[i])
            elif float(list[i]['acousticness']) < smallBoundary*5:
                adjList[4].append(list[i])
            elif float(list[i]['acousticness']) < smallBoundary*6:
                adjList[5].append(list[i])
            elif float(list[i]['acousticness']) < smallBoundary*7:
                adjList[6].append(list[i])
            elif float(list[i]['acousticness']) <smallBoundary*8:
                adjList[7].append(list[i])
            elif float(list[i]['acousticness']) <smallBoundary*9:
                adjList[8].append(list[i])
            else:
                adjList[9].append(list[i])
    elif choice.lower() == "energy":
        print ("You chose energy!")
        for i in range(len(list)):
            if float(list[i]['energy']) <smallBoundary:
                adjList[0].append(list[i])
            elif float(list[i]['energy']) <smallBoundary*2:
                adjList[1].append(list[i])
            elif float(list[i]['energy']) <smallBoundary*3:
                adjList[2].append(list[i])
            elif float(list[i]['energy']) <smallBoundary*4:
                adjList[3].append(list[i])
            elif float(list[i]['energy']) <smallBoundary*5:
                adjList[4].append(list[i])
            elif float(list[i]['energy']) <smallBoundary*6:
                adjList[5].append(list[i])
            elif float(list[i]['energy']) <smallBoundary*7:
                adjList[6].append(list[i])
            elif float(list[i]['energy']) <smallBoundary*8:
                adjList[7].append(list[i])
            elif float(list[i]['energy']) <smallBoundary*9:
                adjList[8].append(list[i])
            else:
                adjList[9].append(list[i])
    elif choice.lower() == "loudness":
        print ("You chose loudness!")
        for i in range(len(list)):
            if abs(float(list[i]['loudness'])) <loudBoundary*9:
                adjList[0].append(list[i])
            elif abs(float(list[i]['loudness'])) <loudBoundary*8:
                adjList[1].append(list[i])
            elif abs(float(list[i]['loudness'])) <loudBoundary*7:
                adjList[2].append(list[i])
            elif abs(float(list[i]['loudness'])) <loudBoundary*6:
                adjList[3].append(list[i])
            elif abs(float(list[i]['loudness'])) <loudBoundary*5:
                adjList[4].append(list[i])
            elif abs(float(list[i]['loudness'])) <loudBoundary*4:
                adjList[5].append(list[i])
            elif abs(float(list[i]['loudness'])) <loudBoundary*3:
                adjList[6].append(list[i])
            elif abs(float(list[i]['loudness'])) <loudBoundary*2:
                adjList[7].append(list[i])
            elif abs(float(list[i]['loudness'])) <loudBoundary*1:
                adjList[8].append(list[i])
            else:
                adjList[9].append(list[i])
    elif choice.lower() == "tempo":
        print ("You chose tempo!")
        for i in range(len(list)):
            if float(list[i]['tempo']) <tempoBoundary:
                adjList[0].append(list[i])
            elif float(list[i]['tempo']) <tempoBoundary*2:
                adjList[1].append(list[i])
            elif float(list[i]['tempo']) <tempoBoundary*3:
                adjList[2].append(list[i])
            elif float(list[i]['tempo']) <tempoBoundary*4:
                adjList[3].append(list[i])
            elif float(list[i]['tempo']) <tempoBoundary*5:
                adjList[4].append(list[i])
            elif float(list[i]['tempo']) <tempoBoundary*6:
                adjList[5].append(list[i])
            elif float(list[i]['tempo']) <tempoBoundary*7:
                adjList[6].append(list[i])
            elif float(list[i]['tempo']) <tempoBoundary*8:
                adjList[7].append(list[i])
            elif float(list[i]['tempo']) <tempoBoundary*9:
                adjList[8].append(list[i])
            else:
                adjList[9].append(list[i])
    else:
        print ("Please select a valid characteristic")
    return adjList

def generate_playlist(list):
    """This function asks the user the size they want their playlist to be
       it then randomly generates a playlist based on the songs they already
       narrowed down and were likely to want to hear"""
    size = input("How many songs in the playlist would you like? ")
    size = int(size)
    playlist = []
    inPlaylist = False
    if size > len(list):
        print ("Sorry but the size of the playlist you requested is too large. Try again.")
    else:
        alreadyIn = []
        while len(playlist) < size:
            index = random.randint(0,size+1)
            inPlaylist = False
            if len(alreadyIn) == 0:
                playlist.append(list[index])
                alreadyIn.append(list[index])
            else:
                for j in range(len(alreadyIn)):
                    if list[index] is alreadyIn[j]:
                        inPlaylist = True
                if inPlaylist == False:
                    playlist.append(list[index])
                    alreadyIn.append(list[index])
    
    return playlist

def playlist_result(playlist):
    #Function prints out the recommended playlist
    print("Here is your recommended playlist!")
    for i in range(len(playlist)):
        print (str(playlist[i]['song_title']) + " by " + str(playlist[i]['artist']))

def runGraphMethod():
    playlist_result(generate_playlist(characteristic_intensity(
        narrow_down(characteristic_intensity(create_like_songs())))))