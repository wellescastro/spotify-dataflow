# Spotify Song Genre Serving Project

This project is responsible for serving predictions for music genre classification of songs.

## Overview

This component is responsible for deploying and serving the trained music genre classification model by providing an API endpoint for real-time genre predictions based on Spotify track features.

This API:
1. Loads the latest model version from MLflow
2. Provides an endpoint for making predictions

## Features

- RESTful API for genre predictions
- Scalable serving architecture
- Open API specification via Swagger API

## Getting Started

### Prerequisites
- Fast API
- Python 3.11+
- Docker (optional)

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

