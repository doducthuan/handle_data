import os
import cv2
import numpy as np
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
from PIL import Image

def get_transforms(image_height, image_width):
    crop_size = min(image_height, image_width, 256)  # Crop động để tránh lỗi
    return A.Compose([
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.2),
        A.RandomBrightnessContrast(p=0.2),
        A.Rotate(limit=30, p=0.5),
        A.GaussianBlur(p=0.2),
        A.Affine(scale=(0.9, 1.1), rotate=(-15, 15), translate_percent=(0.05, 0.05), p=0.5),
        A.PadIfNeeded(min_height=256, min_width=256, border_mode=cv2.BORDER_CONSTANT, p=1.0),
        A.RandomCrop(height=crop_size, width=crop_size, p=0.5),
        ToTensorV2()
    ])

def augment_image(image_path, output_dir, num_augmented=5):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]  # Lấy kích thước ảnh
    transform = get_transforms(h, w)
    
    for i in range(num_augmented):
        augmented = transform(image=image)
        aug_image = augmented['image'].permute(1, 2, 0).numpy() * 255
        aug_image = aug_image.astype(np.uint8)
        aug_image_pil = Image.fromarray(aug_image)
        output_path = os.path.join(output_dir, f"aug_{i}_" + os.path.basename(image_path))
        aug_image_pil.save(output_path)

# Example usage
dataset_path = "path_to_folder_image"
output_path = "path_to_folder_result"
os.makedirs(output_path, exist_ok=True)

for root, _, files in os.walk(dataset_path):
    for file in files:
        if file.lower().endswith(('png', 'jpg', 'jpeg')):
            img_path = os.path.join(root, file)
            augment_image(img_path, output_path)




