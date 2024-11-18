import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def load_nifti_file(nifti_file_path):
    """Load a NIfTI file."""
    print(f"Loading NIfTI file from {nifti_file_path}")
    return nib.load(nifti_file_path)

def extract_corresponding_slices(images_folder, roi_file, output_folder):
    """Extract and save corresponding image and ROI slices."""
    print(f"Processing ROI: {roi_file}")
    roi_nifti = load_nifti_file(roi_file)
    roi_data = roi_nifti.get_fdata()
    print(f"ROI data shape: {roi_data.shape}")

    slice_number = 0
    for image_file in sorted(os.listdir(images_folder)):
        if image_file.endswith('.nii') or image_file.endswith('.nii.gz'):
            image_file_path = os.path.join(images_folder, image_file)
            print(f"Processing image: {image_file_path}")
            image_nifti = load_nifti_file(image_file_path)
            image_data = image_nifti.get_fdata()
            print(f"Image data shape: {image_data.shape}")

            if np.any(roi_data[..., slice_number]):
                print(f"Found ROI at slice {slice_number}, saving...")
                slice_output_path = os.path.join(output_folder, f"slice_{slice_number}.nii.gz")
                nib.save(nib.Nifti1Image(image_data, image_nifti.affine), slice_output_path)
                
                # Visualization for confirmation
                plt.figure(figsize=(10, 5))
                plt.subplot(1, 2, 1)
                plt.imshow(image_data[..., 0], cmap='gray') # Displaying the only slice in the image
                plt.title(f'Image Slice {slice_number}')
                plt.axis('off')

                plt.subplot(1, 2, 2)
                plt.imshow(roi_data[..., slice_number], cmap='gray')
                plt.title(f'ROI Slice {slice_number}')
                plt.axis('off')

                plt.show()
            else:
                print(f"No ROI found at slice {slice_number}")

            slice_number += 1

# Main execution
setup_folder = r'E:\Segmentation\dataset\setup'

# Loop through each patient folder within the setup folder
for patient_folder_name in os.listdir(setup_folder):
    patient_folder_path = os.path.join(setup_folder, patient_folder_name)
    if os.path.isdir(patient_folder_path):
        print(f"Processing patient folder: {patient_folder_name}")
        patient_images_folder = patient_folder_path  # Folder with the patient's 2D image slices
        patient_roi_file = os.path.join(setup_folder, f"{patient_folder_name}.uint16.nii.gz")  # Patient's ROI file
        
        if os.path.isfile(patient_roi_file):
            print(f"Found ROI file for patient: {patient_folder_name}")
            output_folder = os.path.join(patient_folder_path, 'output_slices')  # Folder to save the output slices
            os.makedirs(output_folder, exist_ok=True)

            extract_corresponding_slices(patient_images_folder, patient_roi_file, output_folder)
        else:
            print(f"No ROI file found for patient: {patient_folder_name}")
