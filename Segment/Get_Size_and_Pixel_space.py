import os
import pandas as pd
import pydicom
import nibabel as nib

def get_dicom_info(dicom_file):
    try:
        ds = pydicom.dcmread(dicom_file)
        size = ds.pixel_array.shape
        spacing = ds.PixelSpacing if "PixelSpacing" in ds else [None, None]
        return size, spacing
    except Exception as e:
        print(f"Error reading DICOM file: {dicom_file}. Error: {e}")
        return None, [None, None]

def get_roi_size(roi_file):
    try:
        roi = nib.load(roi_file)
        return roi.get_fdata().shape
    except Exception as e:
        print(f"Error reading ROI file: {roi_file}. Error details: {e}")
        return None

# Base folder containing patient folders
base_folder = r'E:\Segmentation\dataset\setup\Export_DICOMs_and_corresponding_ROIs'

# DataFrame to store the sizes and spacings
data = []

# Iterate over patient folders
for patient_folder in os.listdir(base_folder):
    patient_folder_path = os.path.join(base_folder, patient_folder)
    if os.path.isdir(patient_folder_path):
        for filename in os.listdir(patient_folder_path):
            if filename.lower().endswith('.dcm'):
                dicom_file_path = os.path.join(patient_folder_path, filename)
                dicom_size, pixel_spacing = get_dicom_info(dicom_file_path)

                roi_filename = filename.replace('dicom', 'roi').replace('.dcm', '.nii.gz')
                roi_file_path = os.path.join(patient_folder_path, roi_filename)
                roi_size = None
                if os.path.exists(roi_file_path):
                    roi_size = get_roi_size(roi_file_path)

                data.append({'Patient': patient_folder, 'DICOM File': filename, 
                             'DICOM Size': dicom_size, 'Pixel Spacing': pixel_spacing,
                             'ROI File': roi_filename, 'ROI Size': roi_size})

# Convert to DataFrame
size_df = pd.DataFrame(data)

# Save the DataFrame to a CSV file in the current working directory
output_csv_path = os.path.join(os.getcwd(), 'dicom_roi_sizes.csv')
size_df.to_csv(output_csv_path, index=False)

print(f"Results saved to {output_csv_path}")
