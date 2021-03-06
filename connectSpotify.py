import sys
import spotipy
import spotipy.util as util
import pprint
import csv
import warnings

import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import accuracy_score

import generateConstraints
import GraphStructure

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
  """Constructs a decision tree and prints information
     about its accuracy

    Keyword arguments:
    sp -- the spotipy object
    """
  populate_export_csv(sp)

  data = pandas.read_csv('data/data.csv', usecols = lambda column : column not in 
["song_title" , "artist"])
# data = pandas.read_csv('data/export.csv', usecols = lambda column : column not in 
# ["uri" , "track_href", "analysis_url"])
  print (data.describe())
  print (data.shape)

  train, test = train_test_split(data, test_size=0.15)
  print ("Train size: ", len(train))
  print ("Test size: ", len(test))

  classifier = DecisionTreeClassifier(min_samples_split=100)
  labels = ["duration_ms", "key", "mode", "time_signature", "acousticness", 
            "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "valence", "tempo"]

  x_train = train[labels]
  y_train = train["target"] # we need a field to define whether the user liked the song or not

  x_test = test[labels]
  y_test = test["target"]

  decision_tree = classifier.fit(x_train, y_train)

  y_pred = classifier.predict(x_test)
  print(confusion_matrix(y_test,y_pred))

  score = accuracy_score(y_test, y_pred) * 100

  print ("Accuracy using decision tree: ", round(score, 1), "%")

  return classifier

def nueralNetwork(sp):
  """Constructs a decision tree and prints information
     about its accuracy

    Keyword arguments:
    sp -- the spotipy object
    """
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

def baggingClassifier(sp):
  """Constructs a bagging classifier and prints information
     about its accuracy

    Keyword arguments:
    sp -- the spotipy object
    """
  data = pandas.read_csv('data/data.csv', usecols = lambda column : column not in 
  ["song_title" , "artist"])

  X = data.drop('target',axis=1)
  y = data['target']

  X_train, X_test, y_train, y_test = train_test_split(X, y)

  scaler = StandardScaler()
  scaler.fit(X_train)
  StandardScaler(copy=True, with_mean=True, with_std=True)

  X_train = scaler.transform(X_train)
  X_test = scaler.transform(X_test)

# bagging classifier for ensemble of MLP and decision tree
  #create dictionary for models
  classifier = DecisionTreeClassifier(min_samples_split=100)
  decision_tree = classifier.fit(X_train, y_train)
  mlp = MLPClassifier(hidden_layer_sizes=(13,13,13),max_iter=500)
  mlp.fit(X_train,y_train)

  estimators = { decision_tree, mlp}
  score = 0

  #create bagging classifier
  for base_estimator in estimators:
    ensemble = BaggingClassifier(base_estimator = base_estimator)
    ensemble = ensemble.fit(X_train, y_train)
    predict = ensemble.predict(X_test)
    score += ensemble.score(X_test, y_test)
  
  print(confusion_matrix(y_test,predict))
  print("accuracy of decision tree bagging", score/2)

def songSearch(sp):
  """Allows a user to search spotify for a song and returns 
     three options they can choose from

    Keyword arguments:
    sp -- the spotipy object
    """
  songName = input("Type the name of the song you would like to analyze: ")

  results = sp.search(q=songName, type="track", limit=3)
  items = results['tracks']['items']

  for i in range(0, 3):
    track = items[i]
    artist = track['artists'][0]['name']
    song = track['name']
    
    print ("Is", song, "by", artist, "what you were looking for?")
    proceed = input("(y/n) ")
    proceed = proceed.lower() 

    if proceed == "y":
      features = sp.audio_features(track['id']) 
      df = pandas.DataFrame(features)
      df.to_csv('data/song.csv')
      return pandas.read_csv('data/song.csv', usecols = lambda column : column not in 
                             ["uri" , "track_href", "analysis_url", "id", "type", "duration_ms"])

  print ("Sorry, we couldn't find that song.")


def printWelcome():
  print("     ***** *    **   ***              ***                                                                                             *                          *******                                               ***")
  print("  ******  *  *****    ***              ***                                                            *                       *     **                         *       ***                            *       *      ** ***")
  print(" **   *  *     *****   ***              **                                                           **                      **     **                        *         **                           **      ***    **   ***")
  print("*    *  **     * **      **             **                                                           **                      **     **                        **        *                            **       *     **")
  print("    *  ***     *         **             **                  ****                                   ********    ****        ******** **                         ***             ****       ****     ********         **       **   ****")
  print("   **   **     *         **    ***      **       ****      * ***  * *** **** ****       ***       ********    * ***  *    ********  **  ***      ***          ** ***          * ***  *   * ***  * ********  ***     ******    **    ***  *")
  print("   **   **     *         **   * ***     **      * ***  *  *   ****   *** **** ***  *   * ***         **      *   ****        **     ** * ***    * ***          *** ***       *   ****   *   ****     **      ***    *****     **     ****")
  print("   **   **     *         **  *   ***    **     *   ****  **    **     **  **** ****   *   ***        **     **    **         **     ***   ***  *   ***           *** ***    **    **   **    **      **       **    **        **      **")
  print("   **   **     *         ** **    ***   **    **         **    **     **   **   **   **    ***       **     **    **         **     **     ** **    ***            *** ***  **    **   **    **      **       **    **        **      **")
  print("   **   **     *         ** ********    **    **         **    **     **   **   **   ********        **     **    **         **     **     ** ********               ** *** **    **   **    **      **       **    **        **      **")
  print("    **  **     *         ** *******     **    **         **    **     **   **   **   *******         **     **    **         **     **     ** *******                 ** ** **    **   **    **      **       **    **        **      **")
  print("     ** *      *         *  **          **    **         **    **     **   **   **   **              **     **    **         **     **     ** **                       * *  **    **   **    **      **       **    **        **      **")
  print("      ***      ***      *   ****    *   **    ***     *   ******      **   **   **   ****    *       **      ******          **     **     ** ****    *      ***        *   *******     ******       **       **    **         *********")
  print("       ******** ********     *******    *** *  *******     ****       ***  ***  ***   *******         **      ****            **    **     **  *******      *  *********    ******       ****         **      *** * **           **** ***")
  print("         ****     ****        *****      ***    *****                  ***  ***  ***   *****                                         **    **   *****      *     *****      **                                 ***   **                ***")
  print("                                                                                                                                           *               *                **                                                  *****   ***")
  print("                                                                                                                                          *                 **              **                                                ********  **")
  print("                                                                                                                                         *                                   **                                              *      ****")
  print("                                                                                                                                        *")
  print("")
  print("")
  print("                           ***** *                 *                                                                       **                                ***")
  print("                        ******  *          *     **                                                                     *****                                 ***")
  print("                       **   *  *          ***    **                                                                    *  ***                                  **")
  print("                      *    *  *            *     **                                                                       ***                                  **")
  print("                          *  *                   **         ***  ****               ***  ****    **   ****               *  **                                 **    **   ****        ******             ***  ****")
  print("                         ** **           ***     ** ****     **** **** *    ****     **** **** *  **    ***  *           *  **       ***  ****       ****      **     **    ***  *   ********     ***     **** **** *")
  print("                         ** **            ***    *** ***  *   **   ****    * ***  *   **   ****   **     ****           *    **       **** **** *   * ***  *   **     **     ****   *      **    * ***     **   ****")
  print("                         ** **             **    **   ****    **          *   ****    **          **      **            *    **        **   ****   *   ****    **     **      **           *    *   ***    **")
  print("                         ** **             **    **    **     **         **    **     **          **      **           *      **       **    **   **    **     **     **      **          *    **    ***   **")
  print("                         ** **             **    **    **     **         **    **     **          **      **           *********       **    **   **    **     **     **      **         ***   ********    **")
  print("                         *  **             **    **    **     **         **    **     **          **      **          *        **      **    **   **    **     **     **      **          ***  *******     **")
  print("                            *              **    **    **     **         **    **     **          **      **          *        **      **    **   **    **     **     **      **           *** **          **")
  print("                        ****           *   **    **    **     ***        **    **     ***          *********         *****      **     **    **   **    **     **      *********            ** ****    *   ***")
  print("                       *  *************    *** *  *****        ***        ***** **     ***           **** ***       *   ****    ** *   ***   ***   ***** **    *** *     **** ***           **  *******     ***")
  print("                      *     *********       ***    ***                     ***   **                        ***     *     **      **     ***   ***   ***   **    ***            ***          *    *****")
  print("                      *                                                                             *****   ***    *                                                    *****   ***        *")
  print("                       **                                                                         ********  **      **                                                ********  **        *")
  print("                                                                                                 *      ****                                                         *      ****         *")


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
        select = 0
        classifier = None

        while select is not '6':
          print ("")
          printWelcome()
          print ("How would you like to analyze your library?:")
          print ("[Option 1] song prediction")
          print ("[Option 2] build a decision tree")
          print ("[Option 3] construct a nueral network")
          print ("[Option 4] generate a recommended playlist")
          print("[Option 5] construct an ensemble")
          print("[Option 6] generate playlist from graph structure")
          print ("[Option 7] quit")
          print ("")

          select = input("Choose an option to begin analyzing (1-4): ")

          if select == '1':
            if classifier is not None:
              test = songSearch(sp)
              if classifier.predict(test)[0] is 1:
                print ("I think you would like that song!")
              else:
                print ("I don't think you would like that song.")
            else:
              warnings.warn('Decision Tree or Neural Network must be constructed before predictions can be made.')
          elif select is '2':
            classifier = decisionTree(sp)
          elif select is '3':
            nueralNetwork(sp)
          elif select is '4':
            if classifier is not None:
              #cant store this yet
              generateConstraints.getRecommendedPlaylist(sp, classifier)
            else:
              warnings.warn('Decision Tree or Neural Network must be constructed before predictions can be made.')
          elif select is '5':
            baggingClassifier(sp)
          elif select is '6':
            GraphStructure.runGraphMethod()
          elif select is '7':
            print("Exiting.")
          else:
            print ("Invalid input")

    else:
        print ("Can't get token for", username)

if __name__ == "__main__":
    main()
