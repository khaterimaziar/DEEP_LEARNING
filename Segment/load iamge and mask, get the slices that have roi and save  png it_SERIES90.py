# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 16:12:51 2024

@author: khate
"""

import os
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

# Define paths for images and masks
img_dir = r'E:\Segmentation\dataset\data\PET\raw_images'
mask_dir = r'E:\Segmentation\dataset\data\PET\roi_masks'
main_output_dir = r'E:\Segmentation\dataset\setup'  # Main output directory

# Create output directories if they don't exist
os.makedirs(main_output_dir, exist_ok=True)
output_dir_pet = os.path.join(main_output_dir, 'pet_images')
output_dir_mask = os.path.join(main_output_dir, 'mask_images')
os.makedirs(output_dir_pet, exist_ok=True)
os.makedirs(output_dir_mask, exist_ok=True)

# Get list of patient files
patient_files = os.listdir(r'E:\Segmentation\dataset\DONE')

# Assuming patient files have consistent naming pattern, e.g., 'PET_1.nii.gz', 'WP_1.uint16.nii.gz'
for patient_file in patient_files:
    # Construct paths for PET image and mask
    pet_path = os.path.join(img_dir, patient_file)
    mask_file = patient_file.replace('PET', 'WP').replace('.nii.gz', '.uint16.nii.gz')  # Corrected mask filename
    mask_path = os.path.join(mask_dir, mask_file)

    # Load PET image
    pet_img = nib.load(pet_path)
    pet_data = pet_img.get_fdata()

    # Load mask
    mask_img = nib.load(mask_path)
    mask_data = mask_img.get_fdata()

    # Rotate mask 90 degrees to the right and then flip it
    mask_data = np.rot90(mask_data, k=1)
    mask_data = np.flip(mask_data, axis=0)

    # Display slices with mask
    mask_slices = np.where(np.any(mask_data, axis=(0, 1)))[0]

    for slice_num in mask_slices:
        # Transpose PET image for correct display
        pet_data_transposed = np.transpose(pet_data[:, :, slice_num])

        # Create figure for PET image
        fig, ax = plt.subplots(figsize=(9, 9))
        ax.imshow(pet_data_transposed, cmap='gray')

        # Remove axes and set margins to zero
        ax.axis('off')
        ax.margins(0)

        # Save PET image without whitespace
        output_file_name_pet = f'pet_slice_{patient_file[:-7]}_{slice_num:03}.png'  # Assuming filename ends with '.nii.gz'
        output_path_pet = os.path.join(output_dir_pet, output_file_name_pet)
        fig.savefig(output_path_pet, dpi=300, bbox_inches='tight', pad_inches=0)  # Save PET image without whitespace
        plt.close(fig)  # Close the figure to prevent memory leaks

        # Create figure for mask
        fig, ax = plt.subplots(figsize=(9, 9))
        ax.imshow(mask_data[:, :, slice_num], cmap='gray')

        # Remove axes and set margins to zero
        ax.axis('off')
        ax.margins(0)

        # Save mask without whitespace
        output_file_name_mask = f'mask_slice_{patient_file[:-7]}_{slice_num:03}.png'  # Assuming filename ends with '.nii.gz'
        output_path_mask = os.path.join(output_dir_mask, output_file_name_mask)
        fig.savefig(output_path_mask, dpi=300, bbox_inches='tight', pad_inches=0)  # Save mask without whitespace
        plt.close(fig)  # Close the figure to prevent memory leaks


print(pet_data_transposed.shape)
ax.imshow(pet_data_transposed, cmap='gray')
