import os
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

def standardize_orientation(img, data):
    img = nib.as_closest_canonical(img)
    img_data = data

    # Check if the image is radiologically oriented
    if not nib.orientations.aff2axcodes(img.affine) == ('L', 'A', 'S'):
        # If not, flip the image along the left-right axis
        img_data = np.flip(img_data, axis=0)
        img = nib.Nifti1Image(img_data, img.affine)

    return img, img_data

# Define paths for images and masks
img_dir = r'E:\Segmentation\dataset\data\PET\raw_images'
mask_dir = r'E:\Segmentation\dataset\data\PET\roi_masks'
output_dir = r'E:\Segmentation\dataset\setup'  # Updated output directory

# Load sample image and mask
sample_pet = 'PET_1.nii.gz'
sample_mask = 'WP_1.uint16.nii.gz'

pet_path = os.path.join(img_dir, sample_pet)
mask_path = os.path.join(mask_dir, sample_mask)

# Load PET image and mask
pet_img = nib.load(pet_path)
pet_data = pet_img.get_fdata()
pet_img, pet_data = standardize_orientation(pet_img, pet_data)

mask_img = nib.load(mask_path)
mask_data = mask_img.get_fdata()
mask_img, mask_data = standardize_orientation(mask_img, mask_data)

# Display slices with mask
mask_slices = np.where(np.any(mask_data, axis=(0, 1)))[0]

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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
    output_file_name_pet = f'pet_slice_{slice_num:03}.png'
    output_path_pet = os.path.join(output_dir, output_file_name_pet)
    fig.savefig(output_path_pet, dpi=300, bbox_inches='tight', pad_inches=0)  # Save PET image without whitespace
    plt.close(fig)  # Close the figure to prevent memory leaks

    # Transpose mask data for correct display and apply the same rotation
    mask_data_rotated = np.transpose(mask_data[:, :, slice_num])
    mask_data_rotated = np.flip(mask_data_rotated, axis=0)

    # Create figure for mask
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.imshow(mask_data_rotated, cmap='gray')

    # Remove axes and set margins to zero
    ax.axis('off')
    ax.margins(0)

    # Save mask without whitespace
    output_file_name_mask = f'mask_slice_{slice_num:03}.png'
    output_path_mask = os.path.join(output_dir, output_file_name_mask)
    fig.savefig(output_path_mask, dpi=300, bbox_inches='tight', pad_inches=0)  # Save mask without whitespace
    plt.close(fig)  # Close the figure to prevent memory leaks
