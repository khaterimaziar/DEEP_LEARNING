# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 18:09:35 2024

@author: khate
"""

import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

# Path to the ROI NIfTI file
roi_path = r'E:\Segmentation\dataset\setup\resampled_data\ali\ali_roi_2.nii.gz'  # Replace with your file path

# Load the ROI image using nibabel
roi_nifti = nib.load(roi_path)
roi_image = roi_nifti.get_fdata()

# Convert to a format that can be displayed (if necessary)
roi_image_display = roi_image[:, :, 0] if roi_image.ndim == 3 else roi_image

# Check for unique values
unique_values = np.unique(roi_image)
print("Unique values in the ROI image:", unique_values)

# Displaying the ROI
plt.imshow(roi_image_display, cmap='gray')
plt.title('ROI Image')
plt.axis('off')
plt.show()
