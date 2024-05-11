import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('user_taggedartists.dat', sep='\t')
artists = pd.read_csv('artists.dat', sep='\t')

# Merge data to get artist names
merged_data = pd.merge(data, artists[['id', 'name']], left_on='artistID', right_on='id', how='left')

# Task 10 implemented

# Calculate artist popularity
artist_popularity = merged_data.groupby(['artistID', 'name']).size().reset_index(name='popularity')
artist_popularity = artist_popularity.sort_values(by='popularity', ascending=False)

# Select top 10 popular artists
top_10_popular_artists = artist_popularity.head(10)

# Plot popularity for each artist
for artistID, artist_name in zip(top_10_popular_artists['artistID'], top_10_popular_artists['name']):
    artist_data = merged_data[merged_data['artistID'] == artistID]
    artist_yearly_popularity = artist_data.groupby('year').size()
    artist_yearly_popularity.plot(label=f'{artist_name}')

plt.xlabel('Year')
plt.ylabel('Popularity')
plt.title('Yearly Popularity of Top 10 Artists')
plt.legend()
plt.show()
