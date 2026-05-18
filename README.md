# Airport X-Ray Guard System: Sistem Deteksi Otomatis Ancaman Keamanan Bandara Berbasis YOLO

## Introduction
Sistem kecerdasan buatan yang dirancang untuk mengotomatisasi deteksi barang berbahaya pada pemindai X-ray bandara. Proyek ini menjawab tantangan human error dan kelelahan visual pada proses security screening manual.

## Dataset
Dataset yang digunakan dalam project ini  bisa diakses melalui
- LDXray Dataset : [kaggle](https://www.kaggle.com/datasets/yuzheguocs/LDXray)

## Summary 

Dataset memiliki 12 kelas yang dapat ditampilkan dalam gambar berikut :
![Sample image LDXray dataset FROM : github.com/rstao-bjtu](data/documents/image.png)

Dataset akan memiliki awalan struktur seperti berikut:

```bash
.
├── dataset
│   ├── test_A   # 36.849 gambar (.jpg) tampak atas
│   ├── test_B   # 36.849 gambar (.jpg) tampak samping
│   ├── train_A  # 110.148 gambar (.jpg) tampak atas
│   └── train_B  # 110.148 gambar (.jpg) tampak samping
├── test.json
└── train.json
```
Data annatation tersebut dibungkus dalam format json (`test.json` & `train.json`) yang isinya _(sampel : index 0)_ sebagai berikut:

```json
.json : [
    "annotations" : [
        {
            "id": 1,
            "image_id": 1,
            "category_id": 4,
            "segmentation": [[75,476,75,912,390,912,390,476]],
            "area": 137340,
            "bbox": [75,476,315,436],
            "iscrowd": 0
        },
        ...
        ],
    "categories" : [
        {
            "id": 1,
            "name": "Mobile_Phone",
            "supercategory": "Mobile_Phone"
        },
        ...
        ],
    "images" : [
        {
            "id": 1,
            "width": 440,
            "height": 1040,
            "file_name": "000000.jpg",
            "license": 1,
            "flickr_url": null,
            "coco_url": null,
            "date_captured": "2023-12"
        },
        ...
        ],
    "info" : [...]
    "licenses" : [...]
]
```

yang isinya dapat divisualisasikan dalam gambar berikut:

![](data/documents/erd.svg)

## Struktur Direktori Project

```bash
project
├── configs
│   └── yolo{vesion}{size}.yaml
├── data
│   ├── documents
│   ├── interim
│   ├── processed
│   └── raw
├── notebooks
│   ├── 1_eda.ipynb
│   ├── 2_1_preprocessing_train.ipynb
│   ├── 2_2_preprocessing_test.ipynb
│   └── 3_training.ipynb
└── outputs
    ├── models
    └── logs
```

## Task
- [Done] ------ Data EDA and pre-processing
- [Ongoing] --- Training data
- [Pending] --- App Develop# Airport_X-Ray_Guard_System
