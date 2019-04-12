import sys
import spotipy
import spotipy.util as util
import pprint
import csv

import pandas
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
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
      print sp.audio_features([id])


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

        populate_export_csv(sp)

        data = pandas.read_csv('data/export.csv')
        print data.describe()

        train, test = train_test_split(data, test_size=0.15)
        print ("Train size: ", len(train))
        print ("Test size: ", len(test))

        classifier = DecisionTreeClassifier(min_samples_split=100)
        labels = ["duration_ms", "key", "mode", "time_signature", "acousticness", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "valence", "tempo"]

        # x_train = train[labels]
        # y_train = train["target"] # we need a field to define whether the user liked the song or not

        # x_test = test[labels]
        # y_test = test["target"]

        # decision_tree = classifier.fit(x_train, y_train)

        # y_pred = classifier.predict(x_test)
        # score = accuracy_score(y_test, y_pred) * 100

        # print "Accuracy using decision tree: ", round(score, 1), "%"

    else:
        print "Can't get token for", username

if __name__ == "__main__":
    main()