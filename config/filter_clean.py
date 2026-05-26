import json
import os
import shutil

DATASET_DIR = "dataset" 
OUTPUT_DIR = "filtered_dataset"  
CLASSES = [
    "asparagus", "banana", "broccoli", "carrot", "corn",
    "eggplant", "orange", "pineapple", "potato", "tomato"
]
# ================================

for cls in CLASSES:
    folder_path = os.path.join(DATASET_DIR, cls)
    json_path = os.path.join(folder_path, f"{cls}.json")
    output_path = os.path.join(OUTPUT_DIR, cls)

    # Kiểm tra file JSON tồn tại không
    if not os.path.exists(json_path):
        print(f"[SKIP] Không tìm thấy file JSON cho lớp: {cls}")
        continue

    # Đọc file JSON
    with open(json_path, "r") as f:
        data = json.load(f)

    verified = data.get("verified", [])
    removed = data.get("removed", [])

    # Tạo thư mục output nếu chưa có
    os.makedirs(output_path, exist_ok=True)

    # Copy ảnh verified sang thư mục output
    copied = 0
    not_found = 0
    for filename in verified:
        src = os.path.join(folder_path, filename)
        dst = os.path.join(output_path, filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied += 1
        else:
            not_found += 1

    print(f"[{cls}]")
    print(f"  Verified : {len(verified)} ảnh")
    print(f"  Removed  : {len(removed)} ảnh")
    print(f"  Đã copy  : {copied} ảnh → {output_path}")
    if not_found > 0:
        print(f"  Không tìm thấy: {not_found} ảnh")
    print()

print("Hoàn tất! Ảnh sạch đã được lưu vào:", OUTPUT_DIR)