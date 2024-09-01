import joblib
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

from song_genre_trainer.model.datasets import HoldoutDataset
from song_genre_trainer.spotify_data_loader import SpotifyDataLoader


class SpotifyDataTransformer:
    def __init__(self, data_loader: SpotifyDataLoader) -> None:
        self._data_loader = data_loader

    def prepare_data(
        self, seed=123, save_feature_pipeline=True, feature_pipeline_path=""
    ) -> HoldoutDataset:
        df = self._data_loader.load_data()

        # Preprocess Data
        # Convert genre to binary labels: 1 for 'Happy' and 0 for 'Sad'
        df["genre"] = df["genre"] == "Happy"

        # Feature extraction (assuming text features like song_name or album_name)
        feature_transformer = ColumnTransformer(
            [
                (
                    "song_name_tfidf",
                    TfidfVectorizer(
                        min_df=2,
                        max_features=200,
                        lowercase=True,
                        ngram_range=(1, 3),
                        analyzer="word",
                    ),
                    "song_name",
                ),
                (
                    "algum_name_tfidf",
                    TfidfVectorizer(
                        min_df=2,
                        max_features=200,
                        lowercase=True,
                        ngram_range=(1, 3),
                        analyzer="word",
                    ),
                    "album_name",
                ),
                (
                    "artist_name_tfidf",
                    TfidfVectorizer(
                        min_df=2,
                        max_features=200,
                        lowercase=True,
                        ngram_range=(1, 3),
                        analyzer="word",
                    ),
                    "artist_name",
                ),
            ],
            remainder="drop",
            verbose_feature_names_out=False,
        )
        feature_pipeline = Pipeline(
            [
                ("features", feature_transformer),
            ]
        )

        y = df.pop("genre")
        X = df

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.1, random_state=seed
        )

        feature_pipeline.fit(X_train)

        if save_feature_pipeline and len(feature_pipeline_path) > 0:
            joblib.dump(feature_pipeline, feature_pipeline_path)

        return HoldoutDataset(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
        )
