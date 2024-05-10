import pandas as pd
import matplotlib.pyplot as plt

# task 11 implemented

data = pd.read_csv('user_taggedartists.dat', sep='\t')


artist_popularity = data.groupby('artistID').size().reset_index(name='popularity')


artist_popularity = artist_popularity.sort_values(by='popularity', ascending=False)


top_10_popular_artists = artist_popularity.head(10)


for artistID in top_10_popular_artists['artistID']:
    artist_data = data[data['artistID'] == artistID]
    artist_yearly_popularity = artist_data.groupby('year').size()
    artist_yearly_popularity.plot(label=f'Artist {artistID}')

plt.xlabel('Year')
plt.ylabel('Popularity')
plt.title('Yearly Popularity of Top 10 Artists')
plt.legend()
plt.show()
