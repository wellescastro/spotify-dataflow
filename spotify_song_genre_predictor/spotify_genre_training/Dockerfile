FROM python:3.11

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV PATH="${PATH}:${POETRY_VENV}/bin"
ARG WORKING_DIR="/spotify_genre_training"

ENV MLFLOW_TRACKING_URI=http://mlflow:5000

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
&& $POETRY_VENV/bin/pip install -U pip setuptools \
&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

WORKDIR $WORKING_DIR
COPY README.md pyproject.toml poetry.toml poetry.lock $WORKING_DIR

# Install only the dependencies of the main project
RUN poetry install --only main --no-root --no-directory

COPY ./src/ $WORKING_DIR/src/

RUN poetry check

# Install the main project
RUN poetry install --only main

ENTRYPOINT ["poetry", "run", "train"]

CMD ["--evaluate", "true"]