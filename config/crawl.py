import os
import time
import requests
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def start_crawl(keyword, target_count=100, folder_name=None):
    save_name = folder_name or keyword.split()[0]
    save_dir = os.path.join("dataset", save_name)
    if not os.path.exists(save_dir): os.makedirs(save_dir)

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    downloaded = 0
    page = 1

    try:
        while downloaded < target_count:
            url = f"https://www.freepik.com/search?query={keyword}&page={page}"
            driver.get(url)
            time.sleep(4) 

            for _ in range(5): 
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(1)

            images = driver.find_elements(By.CSS_SELECTOR, "img")
            
            for img in images:
                if downloaded >= target_count: break
                try:
                    src = img.get_attribute("src") or img.get_attribute("data-src")
                    
                    if src and "https://" in src and "static" not in src and "/fps/" not in src:
                        img_data = requests.get(src, timeout=10).content
                        file_name = f"{save_name}_{uuid.uuid4().hex[:8]}.jpg"
                        
                        with open(os.path.join(save_dir, file_name), "wb") as f:
                            f.write(img_data)
                        
                        downloaded += 1
                        print(f"[{downloaded}/{target_count}] Da tai: {file_name}")
                except:
                    continue
            
            print(f"--- Xong trang {page}, dang chuyen sang trang tiep theo... ---")
            page += 1
            if page > 10: break 

    except Exception as e:
        print(f"Loi: {e}")
    finally:
        driver.quit()
        print(f"Tong cong da tai: {downloaded} anh.")

if __name__ == "__main__":
    start_crawl("tomato isolated", target_count=500, folder_name="tomato")
    # Thay từ khóa tìm kiếm (ví dụ: tomato isolated) 
    # và số lượng ảnh muốn crawl (ví dụ: 500)
    # đặt tên thư mục theo từng loại rau củ (ví dụ: tomato)