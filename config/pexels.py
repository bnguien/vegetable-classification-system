import os
import requests
from time import sleep

PEXELS_API_KEY = "uXCzmpaoDukDSSVKzFFuFypzqFnlRjaLE1AFGBXIzmDxPZx5KM719ONn"

CLASSES = {
    "tomato": "fresh tomato",
}

SAVE_DIR = "dataset_raw"
IMAGES_PER_CLASS = 200
PER_PAGE = 80

headers = {
    "Authorization": PEXELS_API_KEY
}

def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
    except Exception as e:
        print("Lỗi tải ảnh:", e)
    return False

def crawl_pexels(class_name, query):
    folder = os.path.join(SAVE_DIR, class_name)
    os.makedirs(folder, exist_ok=True)

    downloaded = 0
    page = 1

    while downloaded < IMAGES_PER_CLASS:
        api_url = "https://api.pexels.com/v1/search"
        params = {
            "query": query,
            "per_page": PER_PAGE,
            "page": page
        }

        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code != 200:
            print("Lỗi API:", response.status_code, response.text)
            break

        data = response.json()
        photos = data.get("photos", [])

        if not photos:
            print(f"Hết ảnh cho lớp {class_name}")
            break

        for photo in photos:
            if downloaded >= IMAGES_PER_CLASS:
                break

            img_url = photo["src"]["large"]
            save_path = os.path.join(folder, f"{class_name}_{downloaded + 1}.jpg")

            if download_image(img_url, save_path):
                downloaded += 1
                print(f"[{class_name}] Đã tải {downloaded}/{IMAGES_PER_CLASS}")

            sleep(0.2)

        page += 1

for class_name, query in CLASSES.items():
    crawl_pexels(class_name, query)

print("Hoàn tất crawl dữ liệu.")