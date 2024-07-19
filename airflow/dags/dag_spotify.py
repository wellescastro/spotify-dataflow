from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup

from util.spotify import SpotifyAPI
from util.storage import Storage

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'dag_spotify',
    default_args=default_args,
    description='Spotify data lake',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=['spotify', 'landing'],
    is_paused_upon_creation=False
) as dag:
    with TaskGroup(group_id='spotify_ingestion') as spotify_ingestion:
        def ingestion(genre: str, s3_path: str):
            api = SpotifyAPI()
            json_data = api.get_top_songs_recommendation(genre=genre)
            storage = Storage()
            storage.save_top_songs_recommendation_to_bucket(data=json_data, path=s3_path)

        PythonOperator(
            task_id='spotify_happy_ingestion',
            python_callable=ingestion,
            op_kwargs={'genre': 'happy', 's3_path': 's3a://landing/spotify_recommend_tracks_happy/'},
        )
        PythonOperator(
            task_id='spotify_sad_ingestion',
            python_callable=ingestion,
            op_kwargs={'genre': 'sad', 's3_path': 's3a://landing/spotify_recommend_tracks_sad/'},
        )
    
    with TaskGroup(group_id='spotify_transformation') as spotify_transformation:
        dbt_build = BashOperator(
            task_id='dbt_build',
            bash_command='cd /opt/airflow/dbt_spotify_manipulator && dbt deps && dbt build --profiles-dir .',
        )

    spotify_ingestion >> spotify_transformation