import os
import nibabel as nib
import numpy as np
from tqdm import tqdm

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
print(f"Found {len(patient_files)} files in the directory.")

# Iterate over patient files
for patient_file in tqdm(patient_files, desc='Processing files'):
   # Construct paths for PET image and mask
   pet_path = os.path.join(img_dir, patient_file)
   mask_file = patient_file.replace('PET', 'WP').replace('.nii.gz', '.uint16.nii.gz')
   mask_path = os.path.join(mask_dir, mask_file)

   # Load PET image and mask
   pet_img = nib.load(pet_path)
   pet_data = pet_img.get_fdata()
   mask_img = nib.load(mask_path)
   mask_data = mask_img.get_fdata()

   # Ensure PET and mask have the same shape
   if pet_data.shape != mask_data.shape:
       raise ValueError('PET image and mask have different shapes.')

   # Find non-empty slices in the mask
   mask_slices = np.where(np.any(mask_data, axis=(0, 1)))[0]

   for slice_num in mask_slices:
       # Transpose PET image for correct display
       pet_data_transposed = np.transpose(pet_data[:, :, slice_num])

       # Save PET image without whitespace
       output_file_name_pet = f'pet_slice_{patient_file[:-7]}_{slice_num:03}.png'
       output_path_pet = os.path.join(output_dir_pet, output_file_name_pet)
       nib.save(nib.Nifti1Image(pet_data_transposed, affine=pet_img.affine), output_path_pet)

       # Save mask without whitespace
       output_file_name_mask = f'mask_slice_{patient_file[:-7]}_{slice_num:03}.png'
       output_path_mask = os.path.join(output_dir_mask, output_file_name_mask)
       nib.save(nib.Nifti1Image(mask_data[:, :, slice_num], affine=mask_img.affine), output_path_mask)

print('Processing completed successfully.')