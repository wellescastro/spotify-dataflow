{{config(
    alias='spotify_recommendations',
    table_type='iceberg'
)}}

select
	*,
	'Happy' as genre
from {{ ref('bronze_spotify_recommendations_happy') }}
union all
select
	*,
	'Sad' as genre
from {{ ref('bronze_spotify_recommendations_sad') }}