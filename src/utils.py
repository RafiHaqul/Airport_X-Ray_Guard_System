# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_json(file_path):
    """Baca file JSON dan kembalikan daftar images serta annotations."""
    with open(file_path, "r") as f:
        data = json.load(f)
    return data["images"], data["annotations"]


def build_image_maps(images):
    """
    Bangun mapping dari image_id ke (nama file tanpa ekstensi, (width, height)).
    """
    return {
        img["id"]: (
            os.path.splitext(img["file_name"])[0],
            (img["width"], img["height"]),
        )
        for img in images
    }


def check_ann_per_image(annotations):
    """
    Kelompokkan anotasi berdasarkan image_id.

    Returns:
        dict: {image_id: [{"category_id": ..., "bbox": ...}, ...]}
    """
    from collections import defaultdict

    ann_per_image = defaultdict(list)
    for ann in annotations:
        ann_per_image[ann["image_id"]].append(
            {"category_id": ann["category_id"], "bbox": ann["bbox"]}
        )
    return ann_per_image


def coco_to_yolo_labels(ann_per_image, id_to_filename_and_size, output_dir):
    """
    Konversi anotasi format COCO ke format YOLO dan simpan ke file .txt.

    Setiap file bernama sesuai nama gambar. Anotasi dengan nilai normalisasi
    di luar rentang [0, 1] akan di-skip.

    Returns:
        tuple: (written_files, skipped_img, skipped_ann)
    """
    os.makedirs(output_dir, exist_ok=True)

    id_to_filename = {
        img_id: info[0] for img_id, info in id_to_filename_and_size.items()
    }
    id_to_size = {
        img_id: info[1] for img_id, info in id_to_filename_and_size.items()
    }

    skipped_img = 0
    skipped_ann = 0
    written_files = 0

    for img_id, anns in ann_per_image.items():
        filename = id_to_filename.get(img_id)
        img_size = id_to_size.get(img_id)

        if not filename or not img_size:
            skipped_img += 1
            continue

        img_w, img_h = img_size
        out_path = os.path.join(output_dir, f"{filename}.txt")
        lines = []

        for ann in anns:
            class_id = ann["category_id"] - 1
            x_min, y_min, bw, bh = ann["bbox"]  # format COCO: [x_min, y_min, w, h]

            cx = x_min + bw / 2  # pusat x
            cy = y_min + bh / 2  # pusat y

            cx_n = cx / img_w   # normalisasi pusat x
            cy_n = cy / img_h   # normalisasi pusat y
            bw_n = bw / img_w   # normalisasi lebar
            bh_n = bh / img_h   # normalisasi tinggi

            if not (0 <= cx_n <= 1 and 0 <= cy_n <= 1 and 0 < bw_n <= 1 and 0 < bh_n <= 1):
                skipped_ann += 1
                continue

            lines.append(f"{class_id} {cx_n:.6f} {cy_n:.6f} {bw_n:.6f} {bh_n:.6f}")

        if lines:
            with open(out_path, "w") as f:
                f.write("\n".join(lines))
            written_files += 1

    return written_files, skipped_img, skipped_ann


def copy_pre_split_images(source, destination, pair):
    """
    Salin gambar dari *source* ke *destination* hanya jika terdapat file
    label (nama dasar sama, ekstensi diabaikan) di direktori *pair*.

    Args:
        source (str): Direktori sumber gambar.
        destination (str): Direktori tujuan.
        pair (str): Direktori label yang menjadi acuan penyalinan.

    Returns:
        str: Path direktori tujuan.

    Raises:
        FileNotFoundError: Jika *source* atau *pair* tidak ditemukan.
    """
    if not os.path.exists(source):
        raise FileNotFoundError(f"Direktori sumber tidak ditemukan: {source}")
    if not os.path.exists(pair):
        raise FileNotFoundError(f"Direktori pasangan (label) tidak ditemukan: {pair}")

    os.makedirs(destination, exist_ok=True)

    label_basenames = {
        os.path.splitext(f)[0]
        for f in os.listdir(pair)
        if os.path.isfile(os.path.join(pair, f))
    }

    copied_count = 0
    for filename in os.listdir(source):
        source_file = os.path.join(source, filename)
        if os.path.isfile(source_file):
            base_name = os.path.splitext(filename)[0]
            if base_name in label_basenames:
                shutil.copy2(source_file, destination)
                copied_count += 1

    print(f"Selesai! Berhasil menyalin {copied_count} gambar dari {source} ke {destination}.")
    return destination


def move_pair(stem, dst_img_dir, dst_lbl_dir):
    """Pindahkan satu pasangan .jpg + .txt ke direktori tujuan."""
    src_img = os.path.join(temp_images_test, stem + ".jpg")
    src_lbl = os.path.join(temp_labels_test, stem + ".txt")
    shutil.move(src_img, os.path.join(dst_img_dir, stem + ".jpg"))
    shutil.move(src_lbl, os.path.join(dst_lbl_dir, stem + ".txt"))


def data_split(stems, img_dst, lbl_dst):
    """Pindahkan pasangan gambar-label ke direktori tujuan."""
    for stem in stems:
        move_pair(stem, img_dst, lbl_dst)
    print(f"{len(stems)} pasangan dipindahkan.")
