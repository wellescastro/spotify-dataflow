import joblib
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    precision_score,
    recall_score,
    accuracy_score,
    f1_score,
)
from sklearn.pipeline import Pipeline
from song_genre_trainer.model.outcome_metrics import OutcomeMetrics
from song_genre_trainer.spotify_data_loader import SpotifyDataLoader
from song_genre_trainer.model.datasets import  HoldoutDataset
from song_genre_trainer.spotify_data_transformer import SpotifyDataTransformer


class MusicGenreClassifier:
    def __init__(self):
        self.final_model = None

    def train(self, data: HoldoutDataset, feature_pipeline_path: str) -> dict:
        X_train, y_train = data.X_train, data.y_train

        param_grid = [
            {"strategy": ["uniform", "stratified"]},
        ]
        model = DummyClassifier()
        grid_search_model = GridSearchCV(
            model, param_grid, cv=5, scoring="f1", refit=True
        )

        feature_pipeline: Pipeline = joblib.load(feature_pipeline_path)
        X_train_transformed = feature_pipeline.transform(X_train)

        grid_search_model.fit(X_train_transformed, y_train)

        self.final_model = Pipeline(
            [
                ("features", feature_pipeline),
                ("model", grid_search_model.best_estimator_),
            ]
        )

        return {
            "model": self.final_model,
            "best_params": grid_search_model.best_params_,
        }

    def evaluate(self, data: HoldoutDataset) -> OutcomeMetrics:
        X_test, y_test = data.X_test, data.y_test
        y_pred = self.final_model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        return OutcomeMetrics(
            accuracy=accuracy, precision=precision, recall=recall, f1_score=f1
        )


if __name__ == "__main__":
    feature_pipeline_path = "./spotify-feature-pipeline.pkl"
    data_loader = SpotifyDataLoader()
    data_transformer = SpotifyDataTransformer(data_loader)
    data = data_transformer.prepare_data(
        save_feature_pipeline=True, feature_pipeline_path=feature_pipeline_path
    )

    classifier = MusicGenreClassifier()
    classifier.train(data, feature_pipeline_path)
    print(classifier.evaluate(data))
