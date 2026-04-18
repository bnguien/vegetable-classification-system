# Models

This folder stores trained machine learning models used for inference.

## Contents
- `.keras` files: Trained CNN models (e.g., ResNet, MobileNet)

## Usage
These models are loaded in the backend (Flask app) to perform image classification.

## Notes
- Ensure the model input size and preprocessing match the training setup.
- Example models:
  - `resnet50.keras`
  - `mobilenetv2.keras`