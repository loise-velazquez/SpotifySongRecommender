import sys
import spotipy
import spotipy.util as util
import pprint
import csv
import Song;

username = "1136204305"

scope = 'user-library-read'
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    songIDs = []
    with open('data/songs.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            songIDs.append(row[0])
    # results = sp.current_user_saved_tracks()
    # for item in results['items']:
    #     track = item['track']
    #     print track['name'] + ' - ' + track['artists'][0]['name']
    # results = sp.search(q='track:' + "Despacito", type='track')
    # pprint.pprint(results)
    for id in songIDs :
      print sp.audio_features([id])

else:
    print "Can't get token for", username