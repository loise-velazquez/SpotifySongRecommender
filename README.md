# SpotifySongRecommender
This is an implementation of a nueral network to create better playlists based on training data supplied from a users
Spotify library.

## Getting Started

First, use the package manager [pip](https://pip.pypa.io/en/stable/) to install Spotipy.
Then, create a [Spotify Developer Account](https://developer.spotify.com/dashboard/login) and retrieve your
unique client id and secret. Next, pick a redirect uri for the API to redirect to after you've been logged
in. http://localhost/ will work fine. Set these values as enviornmental variables before you run.


```bash
pip install spotipy
pip install sklearn
pip install pandas

export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

## Usage

```python
python connectSpotify.py <username>
```

## Authors

* **Olivia Lohe** - [GitHub](https://github.com/OliviaLohe)
* **Nick Bigger** - [GitHub](https://github.com/nbigger)
* **Aaron Thompson** - [GitHub](https://github.com/aroon812)
* **Braden Ash** - [GitHub](https://github.com/ashbraden1)
* **Lukas Jimenez-Smith** - [GitHub](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

## Acknowledgments

* Thank you to the Spotipy team for use of their product, as well as the use of sklearn and pandas.
* Additionally, thank you to Wes Doyle and his YouTube series on how to do machine learning in Python.
