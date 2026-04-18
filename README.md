![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-DeepLearning-orange?style=for-the-badge&logo=tensorflow)
![Keras](https://img.shields.io/badge/Keras-NeuralNetwork-red?style=for-the-badge&logo=keras)
![Flask](https://img.shields.io/badge/Flask-WebApp-black?style=for-the-badge&logo=flask)
![CNN](https://img.shields.io/badge/Model-CNN-green?style=for-the-badge)

# Vegetable Classification System

A lightweight web application that uses deep learning to classify vegetables and fruits from images. The project uses Flask for the web interface and TensorFlow/Keras for model inference, and it is organized to make it easy to add new models or datasets.

Key features
- Upload an image and receive a predicted label
- Supports common CNN architectures (e.g., ResNet, MobileNet)
- Simple, user-friendly web interface

Tech stack
- Python 3.8+
- TensorFlow / Keras
- Flask

Quick start

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv env
env\Scripts\activate   # Windows
pip install -r requirements.txt
```

Run the app:

```bash
python app.py
# Then open http://127.0.0.1:5000 in your browser
```

Usage

- Open the web UI at `http://127.0.0.1:5000`
- Upload an image of a vegetable or fruit
- The app returns a predicted label with confidence score

Training / Adding models

The `models/` directory is intended to store trained models. To train a new model:

1. Prepare a dataset organized by class folders, e.g. `data/train/<class_name>/*.jpg` and `data/val/<class_name>/*.jpg`.
2. Implement a training script (e.g. `train.py`) or adapt utilities in `utils/`.
3. Save the trained model or weights into `models/` and update model-loading code in `app.py`.

Project structure

- `app.py` — Flask application entry point
- `models/` — trained model files
- `notebooks/` — experimentation notebooks (data exploration, preprocessing)
- `static/`, `templates/` — web assets and HTML templates
- `utils/` — helper functions (preprocessing, label mapping, etc.)
- `requirements.txt` — Python dependencies

Requirements

- Python 3.8 or newer
- (Optional) GPU for faster training

Operational notes

- Always activate the virtual environment before installing or running

© Vegetable Classification System
