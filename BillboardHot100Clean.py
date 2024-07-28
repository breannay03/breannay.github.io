import pandas as pd
from collections import Counter
import ast

pd.set_option('display.max_columns', None)

song_features = pd.read_csv('Hot 100 Audio Features.csv')
song_positions = pd.read_csv('Hot Stuff.csv')

all_songs = pd.merge(song_features, song_positions, on="SongID")

# print(all_songs.head(10))

# Scene 1: reorganize to get count of songs of each genre for each year
# Genres: pop, rock, rap, soul, r&b, country
all_songs['Year'] = pd.to_datetime(all_songs['WeekID'], format='%m/%d/%Y').dt.year

all_songs = all_songs[all_songs['Year'] != 2021]

genres = ['pop', 'rock', 'rap', 'soul', 'r&b', 'country']

def parse_genres(genre_str):
    try:
        return ast.literal_eval(genre_str)
    except:
        return []

all_songs['Genres'] = all_songs['spotify_genre'].apply(parse_genres)

all_songs_genres = all_songs.explode('Genres')

all_songs_genres = all_songs_genres[all_songs_genres['Genres'].isin(genres)]

all_songs_genres = all_songs_genres.groupby(['Year', 'Genres']).size().reset_index(name='Unique_Songs')

all_songs_genres.to_csv('Scene1Data.csv')
