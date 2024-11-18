import os
import shutil


data_dir = r"/home/max/Segment/19042024/DONE/"
img_dir = r"E/home/max/Segment/19042024/raw_images"
mask_dir = r"E/home/max/Segment/19042024/roi_masks"

os.makedirs(img_dir, exist_ok=True)
os.makedirs(mask_dir, exist_ok=True)

counter = 1

for folder in os.listdir(data_dir):
    folder_path = os.path.join(data_dir, folder)
    if os.path.isdir(folder_path) and folder != "PET":
        img_files = [f for f in os.listdir(folder_path) if f.endswith(".nii.gz") and "PET" in f]
        mask_files = [f for f in os.listdir(folder_path) if f.endswith(".nii.gz") and "WP" in f]

        if len(img_files) == 1 and len(mask_files) == 1:
            img_file = os.path.join(folder_path, img_files[0])
            img_new_name = f"PET_{counter}.nii.gz"
            img_new_path = os.path.join(img_dir, img_new_name)
            shutil.copyfile(img_file, img_new_path)

            mask_file = os.path.join(folder_path, mask_files[0])
            mask_new_name = f"WP_{counter}.uint16.nii.gz"
            mask_new_path = os.path.join(mask_dir, mask_new_name)
            shutil.copyfile(mask_file, mask_new_path)

            counter += 1
        else:
            print(f"Warning: Incorrect number of files in folder {folder_path}")