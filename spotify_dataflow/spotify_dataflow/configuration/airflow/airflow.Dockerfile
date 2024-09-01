FROM apache/airflow:2.9.2-python3.11

# Configure environment variables and working directory
ENV APP_PATH=/spotify_dataflow
ENV PYTHONPATH=${APP_PATH}
ENV AIRFLOW_HOME=${APP_PATH}/spotify_dataflow/orchestration/airflow
# ENV AIRFLOW__CORE__DAGS_FOLDER=$APP_PATH # Use for custom paths (e.g., you want something other than AIRFLOW_HOME/dags)
WORKDIR ${APP_PATH}

# Copy only requirements for installation
COPY requirements.txt ${APP_PATH}
RUN pip install -r requirements.txt

# Copy the remaining files
COPY . ${APP_PATH}

