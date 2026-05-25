import os
import numpy as np
from PIL import Image
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS so Next.js frontend (on port 3000) can communicate with Flask (on port 5000)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Constants
MODEL_PATH = "models/final_resnet50_model.keras"
IMG_SIZE = (224, 224)

# 10 Class Names sorted alphabetically as Keras's image_dataset_from_directory does:
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

# Detailed premium metadata for each produce item
PRODUCE_INFO = {
    'asparagus': {
        'name': 'Asparagus',
        'vi_name': 'Măng tây',
        'vi_description': 'Măng tây là loại rau cao cấp giàu dinh dưỡng, có vị ngọt nhẹ, giòn sần sật và chứa hàm lượng folate (Vitamin B9) cực cao.',
        'description': 'Asparagus is a premium, nutrient-dense spring vegetable known for its sweet, earthy flavor, tender crunch, and high folate (Vitamin B9) content.',
        'nutrition': {
            'calories': '20 kcal',
            'carbs': '3.9g',
            'protein': '2.2g',
            'fiber': '2.1g',
            'fat': '0.1g'
        },
        'benefits': [
            'Hỗ trợ thai kỳ khỏe mạnh nhờ hàm lượng Folate cực cao.',
            'Cải thiện hệ tiêu hóa, hỗ trợ giảm cân nhờ giàu chất xơ.',
            'Chứa nhiều chất chống oxy hóa giúp làm chậm lão hóa và kháng viêm.'
        ],
        'en_benefits': [
            'Supports healthy pregnancy due to its exceptionally high Folate content.',
            'Improves digestion and aids weight loss through high dietary fiber.',
            'Loaded with antioxidants that fight oxidative stress and inflammation.'
        ],
        'fun_fact': 'Asparagus plants take up to three years from seed to harvest, but once established, they can produce spears for over 15 to 20 years!',
        'vi_fun_fact': 'Cây măng tây phải mất đến 3 năm từ khi gieo hạt mới có thể thu hoạch, nhưng một khi đã trưởng thành, chúng có thể cho thu hoạch liên tục từ 15 đến 20 năm!'
    },
    'banana': {
        'name': 'Banana',
        'vi_name': 'Chuối',
        'vi_description': 'Chuối là loại trái cây nhiệt đới phổ biến bậc nhất thế giới, cung cấp nguồn năng lượng nhanh dồi dào cùng hàm lượng Kali vượt trội.',
        'description': 'Banana is a globally beloved tropical fruit, offering a quick energy boost, natural sweetness, and exceptional potassium content.',
        'nutrition': {
            'calories': '89 kcal',
            'carbs': '22.8g',
            'protein': '1.1g',
            'fiber': '2.6g',
            'fat': '0.3g'
        },
        'benefits': [
            'Cung cấp năng lượng tức thì, rất phù hợp cho người tập thể thao.',
            'Kali giúp ổn định huyết áp, bảo vệ tim mạch hoạt động khỏe mạnh.',
            'Chứa Vitamin B6 dồi dào giúp hỗ trợ phát triển hệ thần kinh.'
        ],
        'en_benefits': [
            'Provides instant and sustained energy, perfect for athletes.',
            'High potassium helps regulate blood pressure and protect heart health.',
            'Rich in Vitamin B6 which supports brain development and nervous system.'
        ],
        'fun_fact': 'Botanically speaking, bananas are actually berries! The banana plant is not a tree, but a large herbaceous flowering plant (herb).',
        'vi_fun_fact': 'Về mặt thực vật học, quả chuối thực chất là một loại quả mọng! Cây chuối cũng không phải là cây thân gỗ mà là cây thân thảo khổng lồ.'
    },
    'broccoli': {
        'name': 'Broccoli',
        'vi_name': 'Súp lơ xanh',
        'vi_description': 'Súp lơ xanh là "siêu thực phẩm" thuộc họ cải, chứa rất nhiều Vitamin C, K và các hợp chất chống ung thư mạnh mẽ.',
        'description': 'Broccoli is a cruciferous superfood packed with essential nutrients, high fiber, and powerful bioactive compounds known to boost immunity.',
        'nutrition': {
            'calories': '34 kcal',
            'carbs': '6.6g',
            'protein': '2.8g',
            'fiber': '2.6g',
            'fat': '0.4g'
        },
        'benefits': [
            'Chứa Sulforaphane - hợp chất chống oxy hóa mạnh mẽ giúp ngăn ngừa ung thư.',
            'Cung cấp Vitamin C vượt trội (nhiều hơn cả cam) giúp tăng sức đề kháng.',
            'Vitamin K và Canxi dồi dào giúp xương và răng chắc khỏe.'
        ],
        'en_benefits': [
            'Contains Sulforaphane, a powerful compound researched for its anti-cancer properties.',
            'Provides more Vitamin C than an orange, significantly boosting the immune system.',
            'Rich in Vitamin K and Calcium, crucial for maintaining strong bones.'
        ],
        'fun_fact': 'Broccoli was originally cultivated by the ancient Romans and has been grown in Europe for over 2,000 years!',
        'vi_fun_fact': 'Súp lơ xanh được người La Mã cổ đại canh tác đầu tiên và đã có lịch sử trồng trọt ở châu Âu hơn 2.000 năm!'
    },
    'carrot': {
        'name': 'Carrot',
        'vi_name': 'Cà rốt',
        'vi_description': 'Cà rốt là loại củ giòn ngọt nổi tiếng giàu Beta-carotene, tiền chất của Vitamin A giúp nuôi dưỡng đôi mắt sáng khỏe.',
        'description': 'Carrot is a sweet, crunchy root vegetable highly celebrated for its Beta-carotene content, which the body converts into eye-protecting Vitamin A.',
        'nutrition': {
            'calories': '41 kcal',
            'carbs': '9.6g',
            'protein': '0.9g',
            'fiber': '2.8g',
            'fat': '0.2g'
        },
        'benefits': [
            'Beta-carotene dồi dào giúp bảo vệ giác mạc, tăng cường thị lực rõ rệt.',
            'Chất chống oxy hóa giúp bảo vệ làn da mịn màng, làm chậm lão hóa.',
            'Chất xơ giúp làm sạch đường ruột, hỗ trợ tim mạch bằng cách giảm cholesterol.'
        ],
        'en_benefits': [
            'Exceptional Beta-carotene levels support healthy vision and night sight.',
            'Antioxidants promote glowing skin and slow down cellular aging.',
            'Soluble fiber aids digestion and helps lower blood cholesterol levels.'
        ],
        'fun_fact': 'The first cultivated carrots were actually purple or yellow, not orange! Orange carrots were bred in the Netherlands in the 17th century.',
        'vi_fun_fact': 'Những củ cà rốt được canh tác đầu tiên trên thế giới có màu tím hoặc màu vàng, chứ không phải màu cam! Cà rốt màu cam được lai tạo ở Hà Lan vào thế kỷ 17.'
    },
    'corn': {
        'name': 'Corn (Maize)',
        'vi_name': 'Ngô (Bắp)',
        'vi_description': 'Ngô là loại ngũ cốc vàng giàu năng lượng, cung cấp chất xơ dồi dào, các chất chống oxy hóa cho mắt và mang vị ngọt tự nhiên hấp dẫn.',
        'description': 'Corn is a globally vital grain that provides natural sweetness, high fiber, energy, and key carotenoids that support vision.',
        'nutrition': {
            'calories': '86 kcal',
            'carbs': '19g',
            'protein': '3.2g',
            'fiber': '2g',
            'fat': '1.2g'
        },
        'benefits': [
            'Chứa Lutein và Zeaxanthin dồi dào giúp phòng ngừa thoái hóa điểm vàng ở mắt.',
            'Cung cấp tinh bột phức hợp lành mạnh, giúp no lâu và nạp năng lượng ổn định.',
            'Giàu chất xơ không hòa tan hỗ trợ hoạt động của lợi khuẩn đường ruột.'
        ],
        'en_benefits': [
            'Rich in Lutein and Zeaxanthin, protecting eyes from age-related macular degeneration.',
            'Provides healthy complex carbohydrates for sustained energy throughout the day.',
            'High in insoluble fiber which feeds beneficial gut bacteria.'
        ],
        'fun_fact': 'An ear of corn always has an even number of rows, usually 16, and there is one piece of silk for every single kernel on the cob!',
        'vi_fun_fact': 'Một bắp ngô luôn luôn có số hàng hạt là một số chẵn (thường là 16), và mỗi một hạt ngô đều được kết nối với đúng một sợi râu ngô!'
    },
    'eggplant': {
        'name': 'Eggplant',
        'vi_name': 'Cà tím',
        'vi_description': 'Cà tím nổi bật với lớp vỏ màu tím bóng loáng giàu chất chống oxy hóa nasunin quý giá giúp bảo vệ tế bào não bộ.',
        'description': 'Eggplant is a versatile nightshade vegetable prized for its glossy purple skin, which is rich in nasunin, a powerful brain-protecting antioxidant.',
        'nutrition': {
            'calories': '25 kcal',
            'carbs': '6g',
            'protein': '1g',
            'fiber': '3g',
            'fat': '0.2g'
        },
        'benefits': [
            'Hợp chất Nasunin trong vỏ bảo vệ lipid màng tế bào não khỏi các gốc tự do.',
            'Hàm lượng calo thấp nhưng giàu chất xơ, lý tưởng cho thực đơn ăn kiêng.',
            'Polyphenol giúp kiểm soát và cải thiện độ nhạy insulin, kiểm soát đường huyết.'
        ],
        'en_benefits': [
            'Nasunin in the skin helps protect brain cell membranes from free radical damage.',
            'Very low in calories yet highly filling due to fiber, perfect for weight management.',
            'Polyphenols promote blood sugar control by improving insulin sensitivity.'
        ],
        'fun_fact': 'In the 18th century, European eggplants were small, white or yellow, and looked exactly like chicken eggs, which is how they got the name "eggplant"!',
        'vi_fun_fact': 'Vào thế kỷ 18 ở châu Âu, quả cà tím có kích thước nhỏ, màu trắng hoặc vàng nhạt, trông giống hệt như quả trứng gà. Đó là lý do chúng có tên tiếng Anh là "eggplant" (quả trứng)!'
    },
    'orange': {
        'name': 'Orange',
        'vi_name': 'Cam',
        'vi_description': 'Cam là loại quả mọng nước ngọt ngào, nổi tiếng khắp thế giới nhờ hàm lượng Vitamin C dồi dào, giúp tăng đề kháng và làm sáng da.',
        'description': 'Orange is a juicy, refreshing citrus fruit famous for its rich Vitamin C levels, boosting immune defense and promoting vibrant skin.',
        'nutrition': {
            'calories': '47 kcal',
            'carbs': '11.8g',
            'protein': '0.9g',
            'fiber': '2.4g',
            'fat': '0.1g'
        },
        'benefits': [
            'Một quả cam đáp ứng hơn 100% nhu cầu Vitamin C hàng ngày của cơ thể.',
            'Giúp thúc đẩy sản sinh collagen cho làn da sáng mịn và nhanh lành vết thương.',
            'Axit citric giúp ngăn ngừa sỏi thận bằng cách làm giảm nồng độ axit trong nước tiểu.'
        ],
        'en_benefits': [
            'A single orange provides over 100% of your daily recommended intake of Vitamin C.',
            'Promotes collagen synthesis for youthful skin and faster healing.',
            'Citric acid reduces risk of kidney stones by raising urinary citrate levels.'
        ],
        'fun_fact': 'Oranges are not wild fruits; they are actually a hybrid cultivated anciently, crossing non-pure citrus fruits: the pomelo and the mandarin!',
        'vi_fun_fact': 'Cam không phải là trái cây mọc hoang dã; chúng thực chất là một giống lai được nuôi cấy từ thời cổ đại giữa bưởi và quýt!'
    },
    'pineapple': {
        'name': 'Pineapple',
        'vi_name': 'Dứa (Thơm / Khóm)',
        'vi_description': 'Dứa là loại quả nhiệt đới ngọt ngào chứa enzyme Bromelain độc đáo, giúp tiêu hóa protein hiệu quả và hỗ trợ kháng viêm.',
        'description': 'Pineapple is a vibrant tropical fruit containing Bromelain, a unique enzyme complex that aids protein digestion and combats inflammation.',
        'nutrition': {
            'calories': '50 kcal',
            'carbs': '13.1g',
            'protein': '0.5g',
            'fiber': '1.4g',
            'fat': '0.1g'
        },
        'benefits': [
            'Enzyme Bromelain tự nhiên giúp phân giải protein, giảm đầy bụng, khó tiêu.',
            'Chất kháng viêm mạnh giúp làm giảm đau khớp, sưng đau sau chấn thương.',
            'Giàu Vitamin C và Mangan hỗ trợ hệ xương chắc khỏe và chuyển hóa năng lượng.'
        ],
        'en_benefits': [
            'Natural Bromelain enzymes break down proteins, facilitating smoother digestion.',
            'Anti-inflammatory properties help alleviate joint pain and swelling.',
            'High Manganese and Vitamin C levels support bone density and metabolic health.'
        ],
        'fun_fact': 'A pineapple is not a single fruit, but a large cluster of individual berries that have fused together around a central core!',
        'vi_fun_fact': 'Một quả dứa thực chất không phải là một trái đơn lẻ, mà là một cụm gồm hàng trăm quả mọng nhỏ kết hợp và hợp nhất xung quanh một lõi trung tâm!'
    },
    'potato': {
        'name': 'Potato',
        'vi_name': 'Khoai tây',
        'vi_description': 'Khoai tây là thực phẩm giàu tinh bột chất lượng cao, chứa hàm lượng Kali và Vitamin C dồi dào, là nguồn cung cấp năng lượng tuyệt vời.',
        'description': 'Potato is a globally popular tuber packed with complex starches, vitamin C, and more potassium than a banana, serving as a clean energy source.',
        'nutrition': {
            'calories': '77 kcal',
            'carbs': '17.5g',
            'protein': '2g',
            'fiber': '2.2g',
            'fat': '0.1g'
        },
        'benefits': [
            'Cung cấp Kali dồi dào giúp cân bằng điện giải và kiểm soát huyết áp.',
            'Chứa tinh bột kháng (resistant starch) hỗ trợ hệ vi sinh đường ruột khỏe mạnh.',
            'Dễ tiêu hóa, cung cấp năng lượng lâu bền phù hợp cho mọi lứa tuổi.'
        ],
        'en_benefits': [
            'Loaded with potassium, essential for healthy blood pressure and fluid balance.',
            'Contains resistant starch which feeds the beneficial bacteria in the gut.',
            'Highly digestible source of clean carbohydrates for sustained fuel.'
        ],
        'fun_fact': 'Potatoes were the first vegetable ever to be grown in outer space, successfully cultivated on the Space Shuttle Columbia in 1995!',
        'vi_fun_fact': 'Khoai tây là loại rau củ đầu tiên trên thế giới được trồng thành công ngoài vũ trụ, trên tàu vũ trụ Columbia vào năm 1995!'
    },
    'tomato': {
        'name': 'Tomato',
        'vi_name': 'Cà chua',
        'vi_description': 'Cà chua mọng nước ngọt ngào, chứa hàm lượng Lycopene cực cao - chất chống oxy hóa tuyệt vời giúp bảo vệ tim mạch và làn da.',
        'description': 'Tomato is a juicy, versatile fruit (used as a vegetable) renowned for its high Lycopene, an antioxidant vital for cardiovascular and skin health.',
        'nutrition': {
            'calories': '18 kcal',
            'carbs': '3.9g',
            'protein': '0.9g',
            'fiber': '1.2g',
            'fat': '0.2g'
        },
        'benefits': [
            'Chất Lycopene dồi dào giúp bảo vệ cơ thể chống lại bệnh tim mạch.',
            'Ăn cà chua giúp tăng cường chống nắng tự nhiên cho da từ sâu bên trong.',
            'Chứa Vitamin A, C, K và Kali tốt cho sức khỏe tim mạch và xương.'
        ],
        'en_benefits': [
            'Rich in Lycopene, a key antioxidant linked to reduced risk of heart disease.',
            'Improves skin health and provides subtle protection against UV rays.',
            'Abundant in vitamins A, C, K, and potassium supporting overall vitality.'
        ],
        'fun_fact': 'In the late 1700s, Europeans called tomatoes the "poison apple" because aristocrats got sick after eating them—unaware that the acidic tomatoes absorbed lead from their pewter plates!',
        'vi_fun_fact': 'Vào cuối thế kỷ 18 ở châu Âu, cà chua được gọi là "quả táo độc". Lý do là vì giới quý tộc ăn xong thường bị ngộ độc, mà không biết rằng tính axit của cà chua đã hòa tan chì từ những chiếc đĩa bằng thiếc-chì của họ!'
    }
}

# Global variable to store loaded model
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
        "produce": PRODUCE_INFO
    })

# Global variable to store other loaded models
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

    # Try to load MobileNet-V2 dynamically if selected
    if model_type == "mobilenetv2":
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
        # Load and convert image to RGB (to drop alpha channel in PNG files)
        img = Image.open(file.stream).convert("RGB")
        
        # Resize to expected shape (MobileNet and ResNet both use 224x224)
        img_resized = img.resize(IMG_SIZE)
        
        # Convert to numpy array
        img_array = np.array(img_resized, dtype=np.float32)
        
        # ResNet50 expects BGR centered preprocessing
        # MobileNet-V2 also typically expects BGR or specific scaling (often [-1, 1])
        # For simplicity and fallback consistency, we preprocess similarly or you can adapt
        # RGB -> BGR
        img_bgr = img_array[..., ::-1]
        
        # Subtract ImageNet channel means: Blue=103.939, Green=116.779, Red=123.68
        img_preprocessed = img_bgr.copy()
        img_preprocessed[..., 0] -= 103.939
        img_preprocessed[..., 1] -= 116.779
        img_preprocessed[..., 2] -= 123.68
        
        # Add batch dimension: (1, 224, 224, 3)
        batch_img = np.expand_dims(img_preprocessed, axis=0)

        # Run prediction on active model (either ResNet or loaded MobileNet)
        predictions = active_model.predict(batch_img)[0]
        
        # Get highest probability index
        predicted_idx = int(np.argmax(predictions))
        confidence = float(predictions[predicted_idx])
        predicted_class = CLASS_NAMES[predicted_idx]

        # Get details for predicted class
        details = PRODUCE_INFO.get(predicted_class, {
            "name": predicted_class.capitalize(),
            "vi_name": predicted_class,
            "description": "Vegetable or Fruit",
            "vi_description": "Trái cây hoặc rau củ quả.",
            "nutrition": {},
            "benefits": [],
            "en_benefits": [],
            "fun_fact": "",
            "vi_fun_fact": ""
        })

        # Return full prediction list sorted by probability
        all_predictions = []
        for i, prob in enumerate(predictions):
            c_name = CLASS_NAMES[i]
            c_details = PRODUCE_INFO.get(c_name, {})
            all_predictions.append({
                "class": c_name,
                "name": c_details.get("name", c_name.capitalize()),
                "vi_name": c_details.get("vi_name", c_name),
                "probability": float(prob)
            })
        
        # Sort predictions descending
        all_predictions = sorted(all_predictions, key=lambda x: x["probability"], reverse=True)

        return jsonify({
            "success": True,
            "class_name": predicted_class,
            "confidence": confidence,
            "details": details,
            "predictions": all_predictions,
            "warning": warning_msg,
            "model_used": "mobilenetv2" if active_model == mobilenet_model else "resnet50"
        })

    except Exception as e:
        print(f"Error during classification: {e}")
        return jsonify({
            "success": False,
            "error": f"An error occurred while processing the image: {str(e)}"
        }), 500

# Remove the template routes since the Next.js app handles the frontend.
# Serve a status dashboard instead at the root if anyone goes to port 5000.
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

# Load the model on startup
load_prediction_model()

if __name__ == "__main__":
    # Disable reload to avoid loading keras model twice in debug mode
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)