import sys
import spotipy
import spotipy.util as util
import pprint
import song;

# export SPOTIPY_CLIENT_ID='195da3e4a242454084d532e399f33123'
# export SPOTIPY_CLIENT_SECRET='1606d6f29ee9448dbb01698f7b271b15'
# export SPOTIPY_REDIRECT_URI='http://localhost/?code=AQBC7UQbpbfT71ylup5VUvhRYZp0ekMhdIv1MC--k0lsjtDyzubG9kSJ7Me3w1t7BsMHMYczJsm-1Osb-NwjbuN-4XWosvdenJXwMYm0_S5Htt_-uulrnhAStp-iizLF9HUWpJKfBwAjcROME4kXbNPGp0DNP9pH0iong7Al_cnkapG2yM3MsoVzZcVtYazLIspTS1K6k867pDOR'
username = "1136204305"

scope = 'user-library-read'
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    songIds = ['6rPO02ozF3bM7NnOV4h6s2', '4uLU6hMCjMI75M1A2tKUQC']
    # results = sp.current_user_saved_tracks()
    # for item in results['items']:
    #     track = item['track']
    #     print track['name'] + ' - ' + track['artists'][0]['name']
    # results = sp.search(q='track:' + "Despacito", type='track')
    # pprint.pprint(results)
    for id in songIds :
      print sp.audio_features([id])

else:
    print "Can't get token for", username