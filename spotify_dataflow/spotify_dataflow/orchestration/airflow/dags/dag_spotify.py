from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from spotify_dataflow.utils.spotify import SpotifyAPI
from spotify_dataflow.utils.storage import Storage

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define keyword arguments to use for all DockerOperator tasks
dockerops_kwargs = {
    "mount_tmp_dir": False,
    "retries": 1,
    "docker_url": "tcp://docker-socket-proxy:2375",
    "network_mode": "container:airflow",
}

interval = timedelta(days=1)
delayed_start_date = days_ago(interval.days) + timedelta(minutes=20)

with DAG(
    "dag_spotify_ingestion",
    default_args=default_args,
    description="Spotify data lake",
    schedule_interval=interval,
    start_date=delayed_start_date,
    tags=["spotify", "landing"],
    is_paused_upon_creation=False,
) as dag:
    with TaskGroup(group_id="spotify_ingestion") as spotify_ingestion:

        def ingestion(genre: str, s3_path: str):
            api = SpotifyAPI()
            json_data = api.get_top_songs_recommendation(genre=genre, quantity=100)
            storage = Storage()
            storage.save_top_songs_recommendation_to_bucket(
                data=json_data, path=s3_path
            )

        PythonOperator(
            task_id="spotify_happy_ingestion",
            python_callable=ingestion,
            op_kwargs={
                "genre": "happy",
                "s3_path": "s3a://landing/spotify_recommend_tracks_happy/",
            },
        )
        PythonOperator(
            task_id="spotify_sad_ingestion",
            python_callable=ingestion,
            op_kwargs={
                "genre": "sad",
                "s3_path": "s3a://landing/spotify_recommend_tracks_sad/",
            },
        )

    with TaskGroup(group_id="spotify_transformation") as spotify_transformation:
        dbt_build = BashOperator(
            task_id="dbt_build",
            bash_command="cd /spotify_dataflow/spotify_dataflow/transformation/dbt/ && dbt deps && dbt build --profiles-dir .",
        )

    trigger_training = TriggerDagRunOperator(
        task_id="trigger_ml_training",
        trigger_dag_id="dag_ml_training",
        conf={"message": "Triggering ml dag"},
    )

    spotify_ingestion >> spotify_transformation >> trigger_training


with DAG(
    "dag_ml_training",
    default_args=default_args,
    description="Machine Learning Model Training",
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=["ml", "training"],
    is_paused_upon_creation=False,
) as dag_ml_training:
    DockerOperator(
        task_id="train_model",
        container_name="spotify-model-training",
        image="spotify-model-training:latest",
        auto_remove=True,
        command="--evaluate true",
        **dockerops_kwargs,
    )
