{{config(
    alias='spotify_recommendations_sad',
    table_type='iceberg'
)}}

WITH unique_songs AS (
    SELECT
        track.id AS song_id,
        track.name AS song_name,
        track.popularity AS song_popularity,
        track.album.name AS album_name,
        track.album.album_type AS album_type,
        artist.name AS artist_name,
        track.href AS spotify_link,
        track.album.images[1].url AS album_image,
        ROW_NUMBER() OVER (PARTITION BY track.id) AS rn
    FROM {{ source('landing', 'spotify_recommend_tracks_sad') }}
    CROSS JOIN UNNEST(tracks) AS track
    CROSS JOIN UNNEST(track.album.artists) AS artist
)

SELECT
    song_id,
    song_name,
    song_popularity,
    album_name,
    album_type,
    artist_name,
    spotify_link,
    album_image
FROM unique_songs
WHERE rn = 1