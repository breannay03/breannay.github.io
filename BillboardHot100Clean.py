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

genres = ['pop', 'rock', 'rap', 'soul', 'r&b', 'country', 'soft rock', 'piano rock', 'pop rock', 'modern rock', ]

def parse_genres(genre_str):
    try:
        return ast.literal_eval(genre_str)
    except:
        return []

all_songs['Genres'] = all_songs['spotify_genre'].apply(parse_genres)

# all_songs_genres = all_songs.explode('Genres')

# all_songs_genres = all_songs_genres[all_songs_genres['Genres'].isin(genres)]

# all_songs_genres = all_songs_genres.groupby(['Year', 'Genres']).size().reset_index(name='Unique_Songs')

# all_songs_genres.to_csv('Scene1Data.csv')

def find_genre(genres_list):
    for genre in genres:
        if genre in genres_list:
            return genre
    return None

all_songs['Genre'] = all_songs['Genres'].apply(find_genre)

all_songs['Genre'] = all_songs['Genre'].replace('soft rock', 'rock')

all_songs['Genre'] = all_songs['Genre'].replace('piano rock', 'rock')

all_songs['Genre'] = all_songs['Genre'].replace('pop rock', 'rock')

all_songs['Genre'] = all_songs['Genre'].replace('modern rock', 'rock')



# Scene 2: reorganize to get info for top 10 artists of all time
# print(all_songs.head(10))

# unique_weeks = all_songs[['Performer_x', 'WeekID']].drop_duplicates()
# artist_week_count = unique_weeks.groupby('Performer_x')['WeekID'].nunique().reset_index()
# artist_week_count.columns = ['Performer_x', 'total_weeks']

# top_10_artists = artist_week_count.nlargest(10, 'total_weeks')['Performer_x']

# top_10_data = all_songs[all_songs['Performer_x'].isin(top_10_artists)]

# top_10_data['Year'] = pd.to_datetime(top_10_data['WeekID']).dt.year

# highest_rank_per_year = top_10_data.groupby(['Performer_x', 'Year']).apply(
#     lambda x: x.loc[x['Peak Position'].idxmin()]
# ).reset_index(drop=True)

# highest_rank_per_year = highest_rank_per_year.merge(artist_week_count, on='Performer_x')

# final_table = highest_rank_per_year[['Performer_x', 'Year', 'Peak Position', 'Song_x', 'Genre', 'total_weeks']]

# final_table.to_csv('Scene2Data.csv')

# Scene 3: get info for top 10 songs of all time

unique_weeks = all_songs[['SongID', 'WeekID']].drop_duplicates()

song_week_count = unique_weeks.groupby('SongID')['WeekID'].nunique().reset_index()
song_week_count.columns = ['SongID', 'total_weeks']

top_10_artists = song_week_count.nlargest(10, 'total_weeks')['SongID']

top_10_data = all_songs[all_songs['SongID'].isin(top_10_artists)]

# top_10_data['Year'] = pd.to_datetime(top_10_data['WeekID']).dt.year

# highest_rank_per_year = top_10_data.groupby(['SongID', 'Year']).apply(
#     lambda x: x.loc[x['Peak Position'].idxmin()]
# ).reset_index(drop=True)

top_10_data = top_10_data.merge(song_week_count, on='SongID')

max_peak_positions = top_10_data.groupby('SongID')['Peak Position'].min().reset_index()
max_peak_positions.columns = ['SongID', 'Max Peak Position']

# Merge the maximum peak position back into the top 10 data
top_10_data = top_10_data.merge(max_peak_positions, on='SongID', how='left')

# Set the peak position to the maximum peak position for each song
top_10_data['Peak Position'] = top_10_data['Max Peak Position']
top_10_data = top_10_data.drop_duplicates(subset=['SongID', 'Year'])

final_table = top_10_data[['Performer_x', 'Year', 'Peak Position', 'SongID', 'Song_x', 'Genre', 'total_weeks']]

final_table.to_csv('Scene3Data.csv')