import numpy as np
from scipy.ndimage import binary_opening, binary_closing, label
import nibabel as nib

def extract_vertebral_body(mask, structure=np.ones((3, 3, 3))):
    # Step 1: Morphological opening to remove thin connections (e.g., pedicles)
    opened_mask = binary_opening(mask, structure=structure)
    
    # Step 2: Connected component analysis to find the largest connected component
    labeled_array, num_features = label(opened_mask)
    component_sizes = np.bincount(labeled_array.ravel())
    component_sizes[0] = 0  # Ignore the background label

    # Identify the label of the largest component
    vertebral_body_label = component_sizes.argmax()
    vertebral_body_mask = (labeled_array == vertebral_body_label).astype(int)

    return vertebral_body_mask

# Load the vertebrae mask (NIfTI file)
#"/Radonc/Cancer Physics and Engineering Lab/Yeseul Kim/Important_Dataset/MDACC/Converted_NIFTIs/Complete/Only_L3Center/456182/Validated_BL_and_PreSurg/BL_CTScans"

file_path = "/Radonc/Cancer Physics and Engineering Lab/Yeseul Kim/Important_Dataset/MDACC/Converted_NIFTIs/Complete/Only_L3Center/456182/Validated_BL_and_PreSurg/PreSurg_CTScans/total_Art_raw.nii.gz/vertebrae_L3.nii.gz"#"path/to/vertebrae_mask.nii.gz"
nifti_img = nib.load(file_path)
vertebrae_mask = nifti_img.get_fdata()

# Extract the vertebral body (spinal body)
spinal_body_mask = extract_vertebral_body(vertebrae_mask)

spinal_body_mask = spinal_body_mask.astype(np.int16)

# Save the result as a new NIfTI file
output_file_path = "/Radonc/Cancer Physics and Engineering Lab/Yeseul Kim/Important_Dataset/MDACC/Converted_NIFTIs/Complete/Only_L3Center/456182/Validated_BL_and_PreSurg/PreSurg_CTScans/extracted_vertebrae_L3.nii.gz"#"path/to/vertebral_body_only.nii.gz"
spinal_body_nifti = nib.Nifti1Image(spinal_body_mask, nifti_img.affine)
nib.save(spinal_body_nifti, output_file_path)
print(f"Vertebral body mask saved as '{output_file_path}'")
