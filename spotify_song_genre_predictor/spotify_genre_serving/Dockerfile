FROM python:3.11

# Variables Section

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache
ENV PATH="${PATH}:${POETRY_VENV}/bin"
ARG WORKING_DIR="/spotify_genre_serving"
ENV MLFLOW_TRACKING_URI=http://mlflow:5000

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

WORKDIR /spotify_genre_serving
COPY README.md pyproject.toml poetry.toml poetry.lock $WORKING_DIR

COPY README.md pyproject.toml poetry.toml poetry.lock $WORKING_DIR

# Install only the dependencies of the main project
RUN poetry install --only main --no-root --no-directory

COPY ./src/ $WORKING_DIR/src/

RUN poetry check

# Install the main project
RUN poetry install --only main

ENTRYPOINT ["poetry", "run", "uvicorn", "song_genre_predictor.main:app", "--host", "0.0.0.0", "--port", "8000"]
