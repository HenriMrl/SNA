import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('user_taggedartists.dat', sep='\t')
artists = pd.read_csv('artists.dat', sep='\t')

merged_data = pd.merge(
    data,
    artists[['id', 'name']],
    left_on='artistID',
    right_on='id',
    how='left'
)

artist_popularity = merged_data \
                    .groupby(['artistID', 'name']) \
                    .size() \
                    .reset_index(name='popularity')

for year in range(2005, 2012):
    plt.figure()
    yearly_data = merged_data[merged_data['year'] == year]
    yearly_popularity = yearly_data \
                    .groupby(['artistID', 'name']) \
                    .size() \
                    .reset_index(name='popularity')
    yearly_popularity = yearly_popularity \
                    .merge(artist_popularity, 
                           on=['artistID', 'name'], 
                           how='inner')
    yearly_popularity = yearly_popularity \
                    .sort_values(by='popularity_x', ascending=False) \
                    .head(10)
    
    plt.bar(yearly_popularity['name'], 
        yearly_popularity['popularity_x'], 
        color='skyblue')
    plt.xlabel('Artist')
    plt.ylabel('Popularity')
    plt.title(f'Top 10 Popular Artists in {year}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

plt.show()
