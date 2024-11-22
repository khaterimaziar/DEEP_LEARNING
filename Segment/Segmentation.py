import os
import dicom
import pydicom
from pydicom.uid import generate_uid
from pydicom.dataset import Dataset
from pydicom.dicomdir import DicomDir

# Specify the path to the DICOM-RT structure set
dicom_rt_path = 'path_to_dicom_rt_structure_set.dcm'

# Load the DICOM-RT structure set
rt_struct = pydicom.dcmread(dicom_rt_path)

# Create a directory to save the 2D ROIs
output_dir = 'output_2d_rois/'
os.makedirs(output_dir, exist_ok=True)

# Iterate through each structure in the RT Structure Set
for structure in rt_struct.StructureSetROISequence:
    structure_name = structure.ROIName
    roi_number = structure.ROINumber

    # Iterate through the contours of the structure
    for contour in rt_struct.ROIContourSequence:
        if contour.ReferencedROINumber == roi_number:
            for contour_sequence in contour.ContourSequence:
                sop_instance_uid = contour_sequence.ContourImageSequence[0].ReferencedSOPInstanceUID
                sop_instance_number = contour_sequence.ContourImageSequence[0].ReferencedFrameNumber

                # Load the corresponding CT image for this contour
                ct_image = pydicom.dcmread(os.path.join('path_to_ct_images/', f'slice{sop_instance_number}.dcm'))

                # Extract the contour data (e.g., pixel coordinates)
                contour_data = contour_sequence.ContourData

                # Create a new DICOM file for the 2D ROI
                new_roi = Dataset()
                new_roi.SOPInstanceUID = generate_uid()
                new_roi.SOPClassUID = '1.2.840.10008.5.1.4.1.1.481.3'  # RT ROI Storage

                # Copy relevant information from the CT image header
                new_roi.PatientName = ct_image.PatientName
                new_roi.PatientID = ct_image.PatientID
                # Copy more relevant attributes...

                # Create a Contour Sequence for the 2D ROI
                new_contour_sequence = Dataset()
                new_contour_sequence.ContourImageSequence = [Dataset()]
                new_contour_sequence.ContourImageSequence[0].ReferencedSOPClassUID = ct_image.SOPClassUID
                new_contour_sequence.ContourImageSequence[0].ReferencedSOPInstanceUID = sop_instance_uid
                # Add more attributes...

                new_roi.ROIContourSequence = [new_contour_sequence]
                # Add more attributes...

                # Save the 2D ROI to the output directory
                output_file = os.path.join(output_dir, f'{structure_name}_slice{sop_instance_number}.dcm')
                new_roi.save_as(output_file)

print("2D ROIs saved to:", output_dir)


