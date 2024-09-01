import pandas as pd
from trino import dbapi


class SpotifyDataLoader:
    def __init__(self) -> None:
        self.trino_host = "trino-coordinator"  # 'trino-coordinator' or 'localhost'
        self.trino_port = 8090  # 8090 for kubernetes or 8085 for host access
        self.trino_user = "admin"
        self.trino_catalog = "minio"
        self.trino_schema = "prod_silver"

    def load_data(self) -> pd.DataFrame:
        trino_conn = self._get_connection()

        query = """
        SELECT
            song_id,
            song_name,
            song_popularity,
            album_name,
            album_type,
            artist_name,
            spotify_link,
            album_image,
            genre
        FROM spotify_recommendations
        """
        cursor = trino_conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(
            rows,
            columns=[
                "song_id",
                "song_name",
                "song_popularity",
                "album_name",
                "album_type",
                "artist_name",
                "spotify_link",
                "album_image",
                "genre",
            ],
        )
        return df

    def _get_connection(self):
        trino_conn = dbapi.connect(
            host=self.trino_host,
            port=self.trino_port,
            user=self.trino_user,
            catalog=self.trino_catalog,
            schema=self.trino_schema,
        )
        return trino_conn
