import sys
import spotipy
import spotipy.util as util
import pprint
import csv
import Song;

def populateSongFile(sp, n):
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

def printSongFile(sp):
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

        populateSongFile(sp, 250)
        printSongFile(sp)

    else:
        print "Can't get token for", username

if __name__ == "__main__":
    main()