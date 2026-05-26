import os
import shutil
from sklearn.model_selection import train_test_split

SOURCE_DIR = "dataset"
OUTPUT_DIR = "vegetable_dataset"

TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

classes = os.listdir(SOURCE_DIR)

for cls in classes:

    class_dir = os.path.join(SOURCE_DIR, cls)

    if not os.path.isdir(class_dir):
        continue

    images = os.listdir(class_dir)

    train_imgs, temp_imgs = train_test_split(
        images,
        test_size=(1 - TRAIN_RATIO),
        random_state=42
    )

    val_imgs, test_imgs = train_test_split(
        temp_imgs,
        test_size=TEST_RATIO / (VAL_RATIO + TEST_RATIO),
        random_state=42
    )

    splits = {
        "train": train_imgs,
        "val": val_imgs,
        "test": test_imgs
    }

    for split_name, split_imgs in splits.items():

        save_dir = os.path.join(OUTPUT_DIR, split_name, cls)
        os.makedirs(save_dir, exist_ok=True)

        for img_name in split_imgs:

            src = os.path.join(class_dir, img_name)
            dst = os.path.join(save_dir, img_name)

            shutil.copy(src, dst)

print("Chia dataset hoàn tất!")