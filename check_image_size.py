import os
from PIL import Image
from collections import Counter

def check_image_sizes(directory, expected_size=(512, 512)):
    size_counter = Counter()
    incorrect_sizes = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                img_path = os.path.join(root, file)
                try:
                    with Image.open(img_path) as img:
                        size = img.size  # (width, height)
                        size_counter[size] += 1
                        if size != expected_size:
                            incorrect_sizes.append((img_path, size))
                except Exception as e:
                    print(f"Error processing {img_path}: {e}")
    
    print("===== Image Size Statistics =====")
    for size, count in size_counter.items():
        print(f"Size {size}: {count} images")   
    print("===== Images with Incorrect Sizes =====")

    for path, size in incorrect_sizes:
        print(f"{path} - {size}")
    
    return size_counter, incorrect_sizes

#Exe
dataset_path = "path_to_folder_image"  
check_image_sizes(dataset_path)
