# Spotify Song Genre Training Project

## Overview
This project is a prototype designed as an exercise to demonstrate how one might structure a machine learning pipeline for classifying songs into genres. **Please note that this project does not use a real machine learning algorithm** due to restrictions in Spotify's API usage policies. Instead, it employs a `DummyClassifier` from scikit-learn, which serves as a baseline model that does not learn from the data.

## Project Structure
- **song_genre_trainer.spotify_data_loader**: Handles data extraction from the Spotify API.
- **song_genre_trainer.spotify_data_transformer**: Prepares and transforms the data into a suitable format for model training.
- **song_genre_trainer.spotify_genre_classifier**: Implements the machine learning model and its evaluation metrics.


## Model Training

The model training process performs the following steps:

1. Loads data from the transformed tables in Trino
2. Prepares features for model training
3. Trains a dummy classifier (as a baseline model)
4. Evaluates the model performance
5. Logs the model and metrics to MLflow

## Dependencies
- Python 3.x
- Click
- MLflow
- Scikit-learn
- Joblib
- Pandas
- Trino

## Getting Started

### Prerequisites

- Python 3.11
- Poetry
- Pipenv (optional)

### Installation
```
poetry install
```

### Running the Project
You can train and evaluate the model by running the main.py script.

```
python train.py --evaluate true --disable_mlflow
```

- --evaluate: Enables model evaluation after training.  
- --disable_mlflow: Disables MLflow tracking if set to True.  


### Model Training
The model is trained using a Dummy classifier (no actual learning conducted) with a pipeline that processes textual features like song names and artist names using TF-IDF.

### Model Evaluation
If the --evaluate flag is set, the model is evaluated on a holdout test set, and metrics such as accuracy, precision, recall, and F1 score are printed.

### MLflow Integration
MLflow is used to log parameters, metrics, and models. You can disable this feature with the --disable_mlflow option.

### Results
The trained model and its performance metrics are saved and tracked in MLflow. The best model is registered and marked as a candidate for further evaluation and potential deployment.


## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

