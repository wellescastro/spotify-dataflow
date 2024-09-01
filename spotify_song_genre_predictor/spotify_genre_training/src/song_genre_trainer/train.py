from typing import Optional
from song_genre_trainer.model.outcome_metrics import OutcomeMetrics
from song_genre_trainer.spotify_genre_classifier import MusicGenreClassifier
from song_genre_trainer.spotify_data_loader import SpotifyDataLoader
from song_genre_trainer.spotify_data_transformer import SpotifyDataTransformer
import click
import mlflow
import mlflow.sklearn
from mlflow import MlflowClient


@click.command()
@click.option(
    "--evaluate",
    type=bool,
    default=False,
    help="Set to true to verify the performance of the trained model.",
)
@click.option(
    "--disable_mlflow",
    is_flag=True,
    help="Enable this flag to disable MLflow logging.",
)
def main(evaluate: bool, disable_mlflow: bool):
    feature_pipeline_path = "spotify-feature-pipeline.pkl"
    data_loader = SpotifyDataLoader()
    data_transformer = SpotifyDataTransformer(data_loader)
    data = data_transformer.prepare_data(
        save_feature_pipeline=True, feature_pipeline_path=feature_pipeline_path
    )

    classifier = MusicGenreClassifier()
    train_data = classifier.train(data, feature_pipeline_path=feature_pipeline_path)

    if evaluate:
        outcomes: OutcomeMetrics = classifier.evaluate(data)
        print(outcomes)

    if not disable_mlflow:
        log_to_mlflow(train_data, outcomes if evaluate else None)


def log_to_mlflow(train_data, outcomes: Optional[OutcomeMetrics] = None):
    mlflow.sklearn.autolog()
    with mlflow.start_run(run_name="naive-bayes-genre-classification", nested=True):
        mlflow.log_param("model_type", "Dummy")
        if outcomes:
            mlflow.log_metrics({
                "accuracy": outcomes.accuracy,
                "precision": outcomes.precision,
                "recall": outcomes.recall,
                "f1_score": outcomes.f1_score
            })

        mlflow.sklearn.log_model(train_data["model"], "model")

        model_name = "spotify-genre-classifier-staging"
        model_version = mlflow.register_model(
            f"runs:/{mlflow.active_run().info.run_id}/model",
            model_name,
        )

        client = MlflowClient()
        client.set_registered_model_alias(
            model_name, "candidate", model_version.version
        )


if __name__ == "__main__":
    main()
