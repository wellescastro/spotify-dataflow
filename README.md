# Spotify Dataflow Solution

This project encompasses a data pipeline and machine learning system for predicting the genre of Spotify songs. It consists of several components that work together to ingest, process, and analyze Spotify data, as well as train and serve a machine learning model for genre prediction.

## Project Structure

The project is divided into three main components:

1. Data Pipeline (spotify_dataflow)
2. Model Training (spotify_genre_training)
3. Model Serving (spotify_genre_serving)

### 1. Data Pipeline (spotify_dataflow)

This component is responsible for ingesting data from the Spotify API, storing it in a data lake, and transforming it for analysis and model training.

Key features:
- Uses Apache Airflow for orchestration
- Stores data in MinIO (S3-compatible object storage)
- Transforms data using dbt (data build tool)
- Uses Trino for distributed SQL queries

This data pipeline is based on the outstanding content created by Victor Outtes (https://nw.ax/s5A). Be sure to check out his work!

### 2. Model Training (spotify_genre_training)

This component trains a machine learning model to predict the genre of songs based on features extracted from the Spotify data.

Key features:
- Uses scikit-learn for model training
- Implements a dummy classifier as a baseline model
- Uses MLflow for experiment tracking and model versioning

See this project's [README](spotify_song_genre_predictor/spotify_genre_training/README.md)

### 3. Model Serving (spotify_genre_serving)

This component serves the trained model as an API for making predictions.

Key features:
- Uses FastAPI to create a RESTful API
- Loads the latest model version from MLflow

See this project's [README](spotify_song_genre_predictor/spotify_genre_serving/README.md)

## Setup and Installation

1. Clone the repository
2. Install Docker and Docker Compose
3. Set up environment variables inside .env file:
   - SPOTIFY_CLIENT_ID
   - SPOTIFY_SECRET

4. Build and start the services:


```1:6:run.sh
# 1. The ML training docker is executed by the Airflow docker instance, so we need to build it before starting docker compose
docker build -t spotify-model-training:latest spotify_song_genre_predictor/spotify_genre_training/

# 2. Start docker compose
docker compose up --build -d --remove-orphans

```


5. Access the various components:
   - Airflow: http://localhost:8080
   - MinIO: http://localhost:9001
   - MLflow: http://localhost:5000
   - Model Serving API: http://localhost:8000

## Data Pipeline

The data pipeline is orchestrated using Apache Airflow. The main DAG performs the following steps:
1. Ingests data from Spotify API
2. Stores raw data in MinIO
3. Transforms data using dbt
4. Triggers the model training process


## Usage

1. Access the Airflow UI to trigger and monitor the data pipeline
2. Use the MLflow UI to view experiment results and model versions
3. Make predictions using the FastAPI endpoint:

```
POST http://localhost:8000/predict
{
    "song_name": "Example Song",
    "album_name": "Example Album",
    "artist_name": "Example Artist"
}
```

## License

This project is licensed under the MIT License.


