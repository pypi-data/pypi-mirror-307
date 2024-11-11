import os
import SimpleITK as sitk

def dicom2nifti(dicom_directory, output_file, verbose = 1):
    if not os.path.exists(output_file):
        # Read the dicom series
        reader = sitk.ImageSeriesReader()
        reader.LoadPrivateTagsOn()
        filenamesDICOM = reader.GetGDCMSeriesFileNames(f'{dicom_directory}')
        reader.SetFileNames(fileNames=filenamesDICOM)
        image = reader.Execute()

        # Save as nifti file
        sitk.WriteImage(image, fileName=output_file)
        print("Converted dicom to nifti >> ", output_file) if verbose > 0 else None
    else:
        print(f"Nifti file '{output_file}' already exists. Skipping conversion.") if verbose > 1 else None

# For a batch run. 
def is_dicom_series(dir_path):
    for file in os.listdir(dir_path):
        if file.endswith(".dcm"):
            return True
        return False

def process_batch_conversion(dir_path, verbose = 1):
    for root, dirs, files in os.walk(dir_path):
        if is_dicom_series(root):
            output_file_name = os.path.basename(root) + ".nii.gz"
            output_file = os.path.join(os.path.dirname(root), output_file_name)

            if os.path.exists(output_file):
                print(f"Nifti file '{output_file}' already exists. Skipping conversion.") if verbose > 0 else None
                continue

            dicom2nifti(root, output_file)

if __name__ == "__main__":
    # Just for test.
    dir_path = "/Radonc/Cancer Physics and Engineering Lab/Yeseul Kim/Important_Dataset/MDACC/pancreas_cancer_DICOM_series/373133/Validated_BL_and_PreSurg/"
    #dicom_dir = os.path.join(dir_path, "Art_recon")
    #nii_file =  os.path.join(dir_path, "Art_recon.nii.gz")

    #dicom2nifti(dicom_dir, nii_file)

    process_batch_conversion(dir_path)








