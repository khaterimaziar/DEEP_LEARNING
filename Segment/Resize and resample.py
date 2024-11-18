import os
import pydicom
import nibabel as nib
from scipy.ndimage import zoom
import cv2
import pandas as pd


# Function to resample images and ROIs
def resample_image(image, current_spacing, target_spacing):
    resampling_factor = [current_spacing[dim] / target_spacing[dim] for dim in range(2)]
    return zoom(image, resampling_factor, order=1)

def resample_roi(roi, current_spacing, target_spacing):
    resampling_factor = [current_spacing[dim] / target_spacing[dim] for dim in range(2)]
    return zoom(roi, resampling_factor, order=0)

# Function to resize images and ROIs
def resize_image(image, target_size):
    return cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)

def resize_roi(roi, target_size):
    return cv2.resize(roi, target_size, interpolation=cv2.INTER_NEAREST)

# Load Patient Data
base_dir = r"E:/Segmentation/dataset/setup/Export_DICOMs_and_corresponding_ROIs"
report_data = []

def load_patient_data(patient_folder):
    dicom_files = [f for f in os.listdir(patient_folder) if f.endswith('.dcm')]
    roi_files = [f for f in os.listdir(patient_folder) if f.endswith('.nii.gz')]
    dicom_files.sort()
    roi_files.sort()

    patient_data = {'images': [], 'rois': [], 'dicom_paths': [], 'spacings': []}
    for dicom_file, roi_file in zip(dicom_files, roi_files):
        dicom_path = os.path.join(patient_folder, dicom_file)
        dicom_data = pydicom.dcmread(dicom_path)
        image = dicom_data.pixel_array
        spacing = list(dicom_data.PixelSpacing)

        roi_path = os.path.join(patient_folder, roi_file)
        roi_data = nib.load(roi_path)
        roi = roi_data.get_fdata()

        patient_data['images'].append(image)
        patient_data['rois'].append(roi)
        patient_data['dicom_paths'].append(dicom_path)
        patient_data['spacings'].append(spacing)

        report_data.append({
            'Patient ID': os.path.basename(patient_folder),
            'Stage': 'Original',
            'Image Size': image.shape,
            'ROI Size': roi.shape,
            'Spacing': spacing
        })

    return patient_data

patient_folders = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
all_data = {}
for folder in patient_folders:
    patient_id = os.path.basename(folder)
    all_data[patient_id] = load_patient_data(folder)

# Resample and Resize Parameters
target_spacing_2d = [1.0, 1.0]  # Target spacing for resampling
target_resize = (256, 256)  # Target size for resizing

# Directory to save the final processed images and ROIs
final_data_dir = r"E:/Segmentation/final_processed_data"  # Update this path as needed
os.makedirs(final_data_dir, exist_ok=True)

# Process Data: Resample, Resize and Save
for patient_id, patient_data in all_data.items():
    patient_dir = os.path.join(final_data_dir, patient_id)
    os.makedirs(patient_dir, exist_ok=True)

    for i, (image, roi, spacing) in enumerate(zip(patient_data['images'], patient_data['rois'], patient_data['spacings'])):
        # Resample
        resampled_image = resample_image(image, spacing, target_spacing_2d)
        resampled_roi = resample_roi(roi, spacing, target_spacing_2d)

        # Resize
        resized_image = resize_image(resampled_image, target_resize)
        resized_roi = resize_roi(resampled_roi, target_resize)

        # Save the final processed image and ROI
        final_image_path = os.path.join(patient_dir, f"{patient_id}_dicom_{i}.png")
        final_roi_path = os.path.join(patient_dir, f"{patient_id}_roi_{i}.png")

        cv2.imwrite(final_image_path, resized_image)
        cv2.imwrite(final_roi_path, resized_roi)

        # Add information to the report
        report_data.append({
            'Patient ID': patient_id,
            'Stage': 'Final Processed',
            'Image Size': resized_image.shape,
            'ROI Size': resized_roi.shape,
            'Spacing': 'N/A'
        })

# Generate Report
report_df = pd.DataFrame(report_data)
report_path = os.path.join(base_dir, 'image_processing_report.csv')
report_df.to_csv(report_path, index=False)

print(f"Report saved to {report_path}")
print(f"Processed images and ROIs saved to {final_data_dir}")
