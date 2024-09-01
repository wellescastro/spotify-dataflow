from typing import Tuple
from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.pipeline import Pipeline
from mlflow.entities.model_registry import ModelVersion

app = FastAPI()


class PredictionRequest(BaseModel):
    song_name: str
    album_name: str
    artist_name: str


def get_latest_model_version(model_name) -> ModelVersion:
    latest_version = None
    mlflow_client = mlflow.MlflowClient()
    for mv in mlflow_client.search_model_versions(f"name='{model_name}'"):
        version_int = int(mv.version)
        if latest_version is None or version_int > int(latest_version.version):
            latest_version = mv
    return latest_version


def load_model_pipeline() -> Tuple[Pipeline, ModelVersion]:
    model_name = "spotify-genre-classifier-staging"
    model_version = get_latest_model_version(model_name)
    model_uri = f"models:/{model_name}/{model_version.version}"
    model: Pipeline = mlflow.sklearn.load_model(model_uri)
    return model, model_version


# TODO: Evolve to use feature store


@app.post("/predict")
def predict(request: PredictionRequest):
    request_map = request.model_dump()
    data = pd.DataFrame([request_map.values()], columns=request_map.keys())

    try:
        model, model_version = load_model_pipeline()
        prediction = model.predict(data)
        return {
            "prediction": int(prediction[0]),
            "model_version": model_version.version,
        }
    except Exception as e:
        return {"error reason": str(e)}


if __name__ == "__main__":
    model = load_model_pipeline()
    print(model)
