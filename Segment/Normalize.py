import numpy as np
import os
import cv2

# Function to load images and ROIs from a directory
def load_images_and_rois(directory):
    images = []
    rois = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.png') or filename.endswith('.jpg'):  # Assuming images are in PNG or JPG format
            img = cv2.imread(os.path.join(directory, filename), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                images.append(img)
            # Assuming corresponding ROI file has a similar name with a different suffix
            roi_filename = filename.replace('.png', '_roi.png').replace('.jpg', '_roi.jpg')
            roi_path = os.path.join(directory, roi_filename)
            if os.path.exists(roi_path):
                roi = cv2.imread(roi_path, cv2.IMREAD_GRAYSCALE)
                rois.append(roi)

    return images, rois

# Directory containing resampled images and ROIs
resampled_base_dir = r'E:\Segmentation\dataset\setup\resampled_data'  # Replace with your directory path

# Load all images and ROIs from the resampled data directory
all_images = []
all_rois = []
for patient_folder in os.listdir(resampled_base_dir):
    patient_folder_path = os.path.join(resampled_base_dir, patient_folder)
    if os.path.isdir(patient_folder_path):
        patient_images, patient_rois = load_images_and_rois(patient_folder_path)
        all_images.extend(patient_images)
        all_rois.extend(patient_rois)

# Convert the lists of images and ROIs to numpy arrays for processing
all_images_array = np.array(all_images)
all_rois_array = np.array(all_rois)

# Calculate the mean and standard deviation across the entire dataset
mean_intensity = np.mean(all_images_array)
std_dev_intensity = np.std(all_images_array)

# Normalize images in the dataset
normalized_images = [(img - mean_intensity) / std_dev_intensity for img in all_images_array]

# Normalizing ROIs might not be necessary if they are binary masks.
# If normalization of ROIs is required, follow a similar approach as images.
# normalized_rois = [(roi - mean_intensity) / std_dev_intensity for roi in all_rois_array]

# Process further or save the normalized images and ROIs as needed
