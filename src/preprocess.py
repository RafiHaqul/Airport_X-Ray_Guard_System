import math
import os

import kagglehub
from src.utils import (
    build_image_maps,
    check_ann_per_image,
    coco_to_yolo_labels,
    copy_pre_split_images,
    data_split,
    read_json
    )

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

# Download latest version
path = kagglehub.dataset_download("yuzheguocs/ldxray")

# Raw data
raw_images_train = path + "/dataset/train_A"
raw_images_test = path + "/dataset/test_A"
raw_labels_train = path + "/train.json"
raw_labels_test = path + "/test.json"

# Temporary data
temp_images_test = "../data/temp/images/test"
temp_labels_test = "../data/temp/labels/test"

# Processed data (siap pakai)
processed_images_train = "../data/processed/images/train"
processed_images_val = "../data/processed/images/val"
processed_images_test = "../data/processed/images/test"
processed_labels_train = "../data/processed/labels/train"
processed_labels_val = "../data/processed/labels/val"
processed_labels_test = "../data/processed/labels/test"

# Rasio split
test_ratio = 0.5
val_ratio = 1 - test_ratio

# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

# Baca metadata
image_train_json, annotation_train_json = read_json(raw_labels_train)
image_test_json, annotation_test_json = read_json(raw_labels_test)

# Bangun mapping id → (filename, size)
test_id_to_filename_and_size = build_image_maps(image_test_json)
train_id_to_filename_and_size = build_image_maps(image_train_json)

# Kelompokkan anotasi per gambar
ann_per_image_test = check_ann_per_image(annotation_test_json)
ann_per_image_train = check_ann_per_image(annotation_train_json)

print(f"Data test memiliki {len(ann_per_image_test)} gambar beranotasi.")
print(f"Data train memiliki {len(ann_per_image_train)} gambar beranotasi.")

# Konversi COCO → YOLO
res_test = coco_to_yolo_labels(
    ann_per_image_test,
    test_id_to_filename_and_size,
    temp_labels_test,
)

# Data train langsung ke folder processed (tidak perlu di-split lagi)
res_train = coco_to_yolo_labels(
    ann_per_image_train,
    train_id_to_filename_and_size,
    processed_labels_train,
)

# Salin gambar sesuai label yang tersedia
copy_pre_split_images(raw_images_test, temp_images_test, temp_labels_test)
copy_pre_split_images(raw_images_train, processed_images_train, processed_labels_train)

# Buat direktori output
for directory in [
    processed_images_test,
    processed_labels_test,
    processed_images_val,
    processed_labels_val,
]:
    os.makedirs(directory, exist_ok=True)

# Kumpulkan pasangan gambar-label yang valid, urutkan secara natural
all_images = sorted(
    f for f in os.listdir(temp_images_test) if f.lower().endswith(".jpg")
)

paired = [
    os.path.splitext(img_file)[0]
    for img_file in all_images
    if os.path.exists(os.path.join(temp_labels_test, os.path.splitext(img_file)[0] + ".txt"))
]

total = len(paired)
n_test = math.floor(total * test_ratio)
n_val = math.floor(total * val_ratio)

test_stems = paired[:n_test]
val_stems = paired[n_test: n_test + n_val]

# Pindahkan ke direktori processed
data_split(test_stems, processed_images_test, processed_labels_test)
data_split(val_stems, processed_images_val, processed_labels_val)

print("Data sudah dipreprocess pada direktori ./data/processed")