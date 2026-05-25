![Python](https://img.shields.io/badge/Python-3.10+-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.21-orange)
![CNN](https://img.shields.io/badge/Model-CNN-green)
![ResNet](https://img.shields.io/badge/ResNet-50-blueviolet)
![Next.js](https://img.shields.io/badge/Next.js-15.0-black)
![Flask](https://img.shields.io/badge/Flask-API-black)

# Vegetable & Fruit Classification System

A premium web application that uses deep learning to classify vegetables and fruits from images. The project uses a **Flask API backend** to run inference on a trained ResNet50 model and a modern **Next.js frontend** for a stunning, bilingual (Vietnamese/English), and highly interactive user experience.

---

## 🌟 Key Features
- **Instant Classification**: Upload an image and receive predicted label with high-speed inference.
- **ResNet50 Model**: High accuracy trained on 10 vegetable and fruit categories.
- **Interactive UI**: Gorgeous glassmorphic card, drag-and-drop zone, and responsive layout matching premium design principles.
- **Rich Nutritional Information**: Displays Calories, Carbs, Protein, Fiber, and Fat per 100g.
- **Bilingual Support**: Toggle seamlessly between Vietnamese and English for all descriptions, benefits, and trivia.
- **Probability Analysis**: Displays confidence score visual breakdown for alternative match predictions.

---

## 🛠️ Supported Produce Categories
The system supports the classification of the following 10 vegetables and fruits:
`Asparagus (Măng tây)`, `Banana (Chuối)`, `Broccoli (Súp lơ xanh)`, `Carrot (Cà rốt)`, `Corn (Ngô/Bắp)`, `Eggplant (Cà tím)`, `Orange (Cam)`, `Pineapple (Dứa/Thơm)`, `Potato (Khoai tây)`, `Tomato (Cà chua)`.

---

## 🚀 How to Run the Project (Hướng Dẫn Chạy Dự Án)

Để ứng dụng hoạt động đầy đủ, bạn cần chạy song song cả **Flask API Backend (Cổng 5000)** và **Next.js Frontend (Cổng 3000)**. Hãy mở **2 cửa sổ Terminal độc lập** để chạy từng phần:

### 1. Khởi động Flask API Backend (Cổng 5000)

**Cửa sổ Terminal 1:**
```bash
# 1. Di chuyển vào thư mục gốc của dự án (nếu chưa có sẵn)
cd vegetable-classification-system

# 2. Kích hoạt môi trường ảo Python Virtual Environment
env\Scripts\activate

# 3. Cài đặt các gói thư viện cần thiết (nếu có cập nhật mới)
pip install -r requirements.txt

# 4. Khởi động Flask API Backend
python app.py
```
*Sau khi chạy thành công, Backend sẽ hoạt động tại địa chỉ: `http://localhost:5000` và tải sẵn mô hình Keras.*

---

### 2. Khởi động Next.js Frontend (Cổng 3000)

**Cửa sổ Terminal 2:**
```bash
# 1. Di chuyển vào thư mục frontend chứa mã nguồn giao diện
cd frontend

# 2. Khởi động chế độ phát triển (Development Mode) của Next.js
npm run dev
```
*Sau khi chạy thành công, giao diện ứng dụng sẽ hoạt động tại địa chỉ: `http://localhost:3000`.*

---

## 💻 Tech Stack Detail

### Backend
- **Python 3.10+**
- **TensorFlow 2.17+** (Inference with Keras ResNet50 model)
- **Flask & Flask-CORS** (RESTful API endpoints)
- **Pillow** (Image preprocessing)

### Frontend
- **Next.js 15+ (App Router)**
- **React 19**
- **Vanilla CSS** (Custom premium glassmorphism styling)
- **Lucide React** (Vector icons)

---

© 2026 VeggieVision AI. Cultivating culinary knowledge.
