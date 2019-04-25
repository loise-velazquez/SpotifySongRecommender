import sys
import spotipy
import spotipy.util as util
import pprint
import csv

import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import accuracy_score

def populate_export_csv(sp):
    """Retrieves users top 50 songs and the corresponding
    audio features and populates a csv to use

    Keyword arguments:
    sp -- the spotipy object
    """
    results = sp.current_user_saved_tracks(50)
    songs = results['items']

    ids = []
    for i in range(len(songs)): 
        ids.append(songs[i]['track']['id']) 

    features = sp.audio_features(ids) 
    df = pandas.DataFrame(features)
    df.to_csv(r'data/export.csv')


def populate_data_file(sp, n):
    """Retrieves the top n songs from the users saved
       tracks, then grabs their IDs and populates
       the data file

    Keyword arguments:
    sp -- the spotipy object
    n -- the number of songs to populate
    """
    offset = 0
    top = n/50 # we fetch 50 songs at a time so divide n by 50
    with open('data/songs.csv', mode='w') as songs_file:
        for x in range(top):
            results = sp.current_user_saved_tracks(50, offset)

            for item in results['items']:
                track = item['track']

                songs_writer = csv.writer(songs_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                trackID = track['id']

                songs_writer.writerow([trackID])

        offset += 50


def get_audio_features(sp):
    """Retrieves the list of songIDs from the data file
       and prints them

    Keyword arguments:
    sp -- the spotipy object
    """
    songIDs = []
    with open('data/songs.csv') as songs_file:
        songs_list = csv.reader(songs_file, delimiter=',')
        for row in songs_list:
            songIDs.append(row[0])

    for id in songIDs :
      print (sp.audio_features([id]))

def decisionTree(sp):
  populate_export_csv(sp)

  data = pandas.read_csv('data/data.csv', usecols = lambda column : column not in 
["song_title" , "artist"])
  print (data.describe())
  print (data.shape)

  train, test = train_test_split(data, test_size=0.15)
  print ("Train size: ", len(train))
  print ("Test size: ", len(test))

  classifier = DecisionTreeClassifier(min_samples_split=100)
  labels = ["duration_ms", "key", "mode", "time_signature", "acousticness", 
            "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "valence", "tempo"]

  # x_train = train[labels]
  # y_train = train["target"] # we need a field to define whether the user liked the song or not

  # x_test = test[labels]
  # y_test = test["target"]

  # decision_tree = classifier.fit(x_train, y_train)

  # y_pred = classifier.predict(x_test)
  # score = accuracy_score(y_test, y_pred) * 100

  # print "Accuracy using decision tree: ", round(score, 1), "%"

def nueralNetwork(sp):
  data = pandas.read_csv('data/data.csv', usecols = lambda column : column not in 
["song_title" , "artist"])
  print (data.describe())
  print (data.shape)

  X = data.drop('target',axis=1)
  y = data['target']

  X_train, X_test, y_train, y_test = train_test_split(X, y)

  scaler = StandardScaler()
  scaler.fit(X_train)
  StandardScaler(copy=True, with_mean=True, with_std=True)

  X_train = scaler.transform(X_train)
  X_test = scaler.transform(X_test)

  mlp = MLPClassifier(hidden_layer_sizes=(13,13,13),max_iter=500)
  mlp.fit(X_train,y_train)

  predictions = mlp.predict(X_test)

  print(confusion_matrix(y_test,predictions))
  print(classification_report(y_test,predictions))

def songSearch(sp):
  songName = input("Type the name of the song you would like to analyze: ")

  results = sp.search(q=songName, type="track", limit=3)
  items = results['tracks']['items']

  if len(items) > 0:
    track = items[0]
    artist = track['artists'][0]['name']
    song = track['name']
    
    print ("Is", song, "by", artist, "what you were looking for?")
    proceed = input("(y/n) ")
    proceed = proceed.lower() 

    if proceed == "y":
      print ("")

    elif proceed == "n":
      print ("")

  else:
    print ("Sorry, we couldn't find that song.")

def main():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        # print "Usage: %s username" % (sys.argv[0],)
        # sys.exit()
        username = "1136204305"

    scope = 'user-library-read'
    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)

        print ("========== Welcome to the Spotify Library Analyzer ==========")
        print ("How would you like to analyze your library?:")
        print ("[Option 1] search for a song")
        print ("[Option 2] build a decision tree")
        print ("[Option 3] construct a nueral network")
        print ("")

        select = input("Choose an option to begin analyzing (1-3): ")

        switch = {
          1: songSearch,
          2: decisionTree,
          3: nueralNetwork
        }

        if select == '1':
          songSearch(sp)
        elif select == '2':
          decisionTree(sp)
        elif select == '3':
          nueralNetwork(sp)
        else:
          print ("Invalid input")

    else:
        print ("Can't get token for", username)

if __name__ == "__main__":
    main()