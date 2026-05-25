import os
import numpy as np
from PIL import Image
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

MODEL_PATH = "models/final_resnet50_model.keras"
IMG_SIZE = (224, 224)

CLASS_NAMES = [
    'asparagus', 
    'banana', 
    'broccoli', 
    'carrot', 
    'corn', 
    'eggplant', 
    'orange', 
    'pineapple', 
    'potato', 
    'tomato'
]
VEGGIE_NAMES = {
    'asparagus': {'name': 'Asparagus', 'vi_name': 'Măng tây'},
    'banana': {'name': 'Banana', 'vi_name': 'Chuối'},
    'broccoli': {'name': 'Broccoli', 'vi_name': 'Súp lơ xanh'},
    'carrot': {'name': 'Carrot', 'vi_name': 'Cà rốt'},
    'corn': {'name': 'Corn', 'vi_name': 'Bắp'},
    'eggplant': {'name': 'Eggplant', 'vi_name': 'Cà tím'},
    'orange': {'name': 'Orange', 'vi_name': 'Cam'},
    'pineapple': {'name': 'Pineapple', 'vi_name': 'Dứa'},
    'potato': {'name': 'Potato', 'vi_name': 'Khoai tây'},
    'tomato': {'name': 'Tomato', 'vi_name': 'Cà chua'}
}

model = None

def load_prediction_model():
    global model
    if model is None:
        print(f"--- Loading Keras Model from {MODEL_PATH} ---")
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
            print("--- Keras Model loaded successfully! ---")
        except Exception as e:
            print(f"Error loading model: {e}")

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "classes": CLASS_NAMES
    })

@app.route("/api/info", methods=["GET"])
def info():
    return jsonify({
        "success": True,
        "produce": VEGGIE_NAMES
    })

mobilenet_model = None

@app.route("/api/classify", methods=["POST"])
def classify():
    global mobilenet_model
    
    if model is None:
        return jsonify({
            "success": False,
            "error": "Model is not loaded on backend. Please try again in a few moments."
        }), 500

    if "image" not in request.files:
        return jsonify({
            "success": False,
            "error": "No image file provided in request."
        }), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({
            "success": False,
            "error": "Empty filename."
        }), 400

    model_type = request.form.get("model", "resnet50")
    active_model = model
    warning_msg = None

    if model_type == "mobilenetv2":
        mobilenet_path = "models/best_mobilenetv2_model_2.keras"
        if not os.path.exists(mobilenet_path):
            mobilenet_path = "models/final_mobilenetv2_model.keras"
        if os.path.exists(mobilenet_path):
            if mobilenet_model is None:
                try:
                    print(f"--- Loading Keras MobileNetV2 Model from {mobilenet_path} ---")
                    mobilenet_model = tf.keras.models.load_model(mobilenet_path)
                    print("--- Keras MobileNetV2 Model loaded successfully! ---")
                except Exception as e:
                    print(f"Error loading MobileNet model: {e}")
            if mobilenet_model is not None:
                active_model = mobilenet_model
            else:
                warning_msg = "Mô hình MobileNet-V2 đang được phát triển. Hệ thống tự động chuyển sang mô hình ResNet-50."
        else:
            warning_msg = "Mô hình MobileNet-V2 đang được phát triển. Hệ thống tự động chuyển sang mô hình ResNet-50."

    try:
        img = Image.open(file.stream).convert("RGB")
        
        img_resized = img.resize(IMG_SIZE)
        
        img_array = np.array(img_resized, dtype=np.float32)

        if active_model == mobilenet_model:
            img_preprocessed = (img_array / 127.5) - 1.0
        else:
            img_bgr = img_array[..., ::-1]
            img_preprocessed = img_bgr.copy()
            img_preprocessed[..., 0] -= 103.939
            img_preprocessed[..., 1] -= 116.779
            img_preprocessed[..., 2] -= 123.68
        
        batch_img = np.expand_dims(img_preprocessed, axis=0)

        import time
        t_start = time.perf_counter()
        predictions = active_model.predict(batch_img)[0]
        inference_time = time.perf_counter() - t_start
        
        predicted_idx = int(np.argmax(predictions))
        confidence = float(predictions[predicted_idx])
        predicted_class = CLASS_NAMES[predicted_idx]

        details = VEGGIE_NAMES.get(predicted_class, {
            "name": predicted_class.capitalize(),
            "vi_name": predicted_class
        })

        all_predictions = []
        for i, prob in enumerate(predictions):
            c_name = CLASS_NAMES[i]
            c_details = VEGGIE_NAMES.get(c_name, {
                "name": c_name.capitalize(),
                "vi_name": c_name
            })
            all_predictions.append({
                "class": c_name,
                "name": c_details.get("name"),
                "vi_name": c_details.get("vi_name"),
                "probability": float(prob)
            })
        
        all_predictions = sorted(all_predictions, key=lambda x: x["probability"], reverse=True)

        return jsonify({
            "success": True,
            "class_name": predicted_class,
            "confidence": confidence,
            "details": details,
            "predictions": all_predictions,
            "warning": warning_msg,
            "model_used": "mobilenetv2" if active_model == mobilenet_model else "resnet50",
            "inference_time": inference_time
        })

    except Exception as e:
        print(f"Error during classification: {e}")
        return jsonify({
            "success": False,
            "error": f"An error occurred while processing the image: {str(e)}"
        }), 500

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Vegetable Classification System Flask API",
        "status": "online",
        "api_endpoints": [
            "GET /api/health - Check model status",
            "GET /api/info - Get detailed nutrition/fact database",
            "POST /api/classify - Classify vegetable image"
        ]
    })

load_prediction_model()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)