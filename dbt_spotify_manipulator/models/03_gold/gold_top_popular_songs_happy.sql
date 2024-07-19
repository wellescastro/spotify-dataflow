{{config(
    alias='top_popular_songs_happy',
    table_type='iceberg'
)}}

select
	song_name,
	artist_name,
	album_name,
	album_image,
	song_popularity
from {{ ref('silver_spotify_recommendations') }}
where genre = 'Happy'
order by song_popularity desc
limit 5