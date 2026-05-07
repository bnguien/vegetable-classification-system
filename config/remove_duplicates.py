import hashlib
import os

def get_image_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def remove_duplicates(folder_path):
    hashes = {}
    duplicates_count = 0
    
    print(f"--- Đang quét thư mục: {folder_path} ---")

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            file_hash = get_image_hash(file_path)
            
            if file_hash in hashes:
                print(f"[XÓA] {filename} là bản sao của {hashes[file_hash]}")
                os.remove(file_path)
                duplicates_count += 1
            else:
                hashes[file_hash] = filename

    print(f"--- Hoàn tất! Đã xóa {duplicates_count} ảnh trùng lặp ---")

if __name__ == "__main__":
    TARGET_FOLDER = "dataset/tomato" # thay đổi tên theo loại vegetable đã crawl
    remove_duplicates(TARGET_FOLDER)