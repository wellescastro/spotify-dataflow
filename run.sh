# 1. The ML training docker is executed by the Airflow docker instance, so we need to build it before starting docker compose
docker build -t spotify-model-training:latest spotify_song_genre_predictor/spotify_genre_training/

# 2. Start docker compose
docker compose up --build -d --remove-orphans
