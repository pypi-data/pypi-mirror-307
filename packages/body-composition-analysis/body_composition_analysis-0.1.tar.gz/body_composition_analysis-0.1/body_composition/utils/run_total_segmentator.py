import os
from totalsegmentator.python_api import totalsegmentator

def shorten_filename(file_path, fName_max_length=250, verbose = 1):
    # If the name is too long, will give you error. 
     if len(file_path) >= fName_max_length:
        print(f"File name is too long, so shortened: {file_path}") if verbose > 0 else None
        return file_path[:fName_max_length]
     else:
        return file_path
     
def run_total_segmentator(nii_path, task:str, get_statistics: bool, fName_max_length=250, verbose = 1):
    # run TotalSegmentator for each task. 
    seg_dir_path = shorten_filename(os.path.join(os.path.dirname(nii_path), task+"_"+ os.path.basename(nii_path)), fName_max_length=fName_max_length)
    if not os.path.exists(seg_dir_path):
        try:
            totalsegmentator(nii_path, seg_dir_path, device='gpu', task = task, statistics=get_statistics)
            return seg_dir_path
        except Exception as e:
            print(f"An unexpected error occurred: {e}") if verbose > 0 else None
            return None
    else:
        print(f"Output directory '{seg_dir_path}' already exists. Skipping.") if verbose > 0 else None
        return seg_dir_path

def run_segmentator_for_body_comp(nii_path, get_statistics=False, verbose = 1):
    total_seg_dir_path = run_total_segmentator(nii_path=nii_path, task='total', get_statistics=get_statistics, verbose=verbose) # Run for the whole segmentation.
    tissue_seg_dir_path = run_total_segmentator(nii_path=nii_path, task='tissue_types', get_statistics=get_statistics, verbose=verbose) # Run for the tissue composition. 
    body_seg_dir_path = run_total_segmentator(nii_path=nii_path, task='body', get_statistics=get_statistics, verbose=verbose) # Run for the body cavity segmentation.
    return (total_seg_dir_path, tissue_seg_dir_path, body_seg_dir_path)

if __name__ == "__main__":
    # Just for test.
    dir_path = "/Radonc/Cancer Physics and Engineering Lab/Yeseul Kim/Important_Dataset/MDACC/pancreas_cancer_DICOM_series/373133/Validated_BL_and_PreSurg/BL_CTScans"
    #dicom_dir = os.path.join(dir_path, "Art_recon")
    nii_file =  os.path.join(dir_path, "Art_recon.nii.gz")

    run_segmentator_for_body_comp(nii_file)


