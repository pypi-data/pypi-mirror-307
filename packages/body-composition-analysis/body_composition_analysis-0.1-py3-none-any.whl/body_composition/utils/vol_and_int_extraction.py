import os
import numpy as np
import SimpleITK as sitk

def get_img_and_arr_from_nii(nii_path):
    img = sitk.ReadImage(nii_path)
    arr = sitk.GetArrayFromImage(img)
    return img, arr

# Get volumes and intensity for roi types

# 1) Organ: liver, pancreas
def is_organ_truncated(arr):
    top_axial_view = arr[0, :, :]
    bottom_axial_view = arr[arr.shape[0]-1, :, :]
    if np.sum(top_axial_view) != 0 or np.sum(bottom_axial_view) !=0:
        return True
    else:
        return False

def get_volume_from_mask_nii(img, arr):
    #img, arr = get_img_and_arr_from_nii(nii_path=nii_path)
    spacing = img.GetSpacing()
    voxel_volume = spacing[0]*spacing[1]*spacing[2]
    voxel_count = np.sum(arr ==1)
    roi_volume = round(voxel_count * voxel_volume, 4)
    is_truncated = is_organ_truncated(arr)
    return (roi_volume, is_truncated)

def get_intensity(ct_arr, roi_arr):
    #ct_img, ct_arr = get_img_and_arr_from_nii(nii_path=ct_nii_path)
    #roi_img, roi_arr = get_img_and_arr_from_nii(nii_path=mask_nii_path)
    roi_ct_arr = ct_arr[roi_arr > 0]
    avg_intensity, std_intensity = round(np.mean(roi_ct_arr),4), round(np.std(roi_ct_arr),4)
    return avg_intensity, std_intensity


# 2) Tissue composition: visceral abdominal fat (VAF), subcutaneous abdominal fat (SAF), skeletal muscle area (SMA)
def find_cetner_of_vertebrae(arr):
    bottom, center, top, notes = None, None, None, None
    #img, arr = get_img_and_arr_from_nii(nii_path=nii_path)
    if np.sum(arr) != 0:
        zs = []
        for x in range(len(arr)):
            if np.sum(arr[x, :, :]) > 0.5:
                zs.append(x)
        if len(zs) > 0:
            bottom = np.min(zs)
            top = np.max(zs)
            center = round((bottom + top) / 2)
            notes = True
            return (bottom, center, top, notes)
    else:
        notes = False
        return (bottom, center, top, notes)
    
def get_center_L3(total_seg_dir_path):
    l3_nii_path = os.path.join(total_seg_dir_path, "vertebrae_L3.nii.gz")
    _, l3_arr = get_img_and_arr_from_nii(l3_nii_path)
    bottom, center, top, notes = find_cetner_of_vertebrae(l3_arr)
    if notes == True:
        notes = 'L3'
        return (bottom, center, top, notes)
    else:
        l2_nii_path = os.path.join(total_seg_dir_path, "vertebrae_L2.nii.gz")
        _, l2_arr = get_img_and_arr_from_nii(l2_nii_path)
        bottom, center, top, notes = find_cetner_of_vertebrae(l2_arr)
        if notes == True:
            notes = 'L2'
            return (bottom, center, top, notes) 
        else:
            l1_nii_path = os.path.join(total_seg_dir_path, "vertebrae_L1.nii.gz")
            _, l1_arr = get_img_and_arr_from_nii(l1_nii_path)
            bottom, center, top, notes = find_cetner_of_vertebrae(l1_arr)
            notes = 'L1'
            return (bottom, center, top, notes) 

def get_roi_center_L3_arr(roi_arr, l3_center:int):
    roi_center_L3_arr = roi_arr[l3_center, :, :]
    return roi_center_L3_arr

def get_area_and_axial_thickness_at_center_L3(roi_img, roi_arr, l3_center:int):
    roi_center_L3_arr = get_roi_center_L3_arr(roi_arr=roi_arr, l3_center=l3_center)
    roi_spacing = roi_img.GetSpacing()
    pixel_size = roi_spacing[0] * roi_spacing[1]
    slice_thickness = roi_spacing[2]

    roi_pixel_counts = np.sum(roi_center_L3_arr == 1)
    roi_area_at_center_L3 = round(roi_pixel_counts * pixel_size, 4)
    return (roi_area_at_center_L3, slice_thickness)

def get_intensity_at_center_L3(ct_arr, roi_arr, l3_center:int):
    roi_ct_arr = np.where(roi_arr > 0, ct_arr, 0) 
    roi_ct_center_L3_arr = get_roi_center_L3_arr(roi_arr=roi_ct_arr, l3_center=l3_center)
    avg_intensity, std_intensity = round(np.mean(roi_ct_center_L3_arr),4), round(np.std(roi_ct_center_L3_arr),4)
    return (avg_intensity, std_intensity)
    

if __name__ == "__main__":
    # Just for test.
    dir_path = "/Radonc/Cancer Physics and Engineering Lab/Yeseul Kim/Important_Dataset/MDACC/Converted_NIFTIs/Complete/Only_L3Center/456182/Validated_BL_and_PreSurg/BL_CTScans"

    ct_nii_path = os.path.join(dir_path, "Art_recon.nii.gz")
    ct_img, ct_arr = get_img_and_arr_from_nii(ct_nii_path)
    liver_nii_path = os.path.join(dir_path, "SegWh_Art_recon.nii.gz", "liver.nii.gz")
    liver_img, liver_arr = get_img_and_arr_from_nii(liver_nii_path)
    total_seg_dir_path = os.path.join(dir_path, "SegWh_Art_recon.nii.gz")




    bottom, center, top, notes = get_center_L3(total_seg_dir_path=total_seg_dir_path)

    '''tissue_dir_path = os.path.join(dir_path, "SegTs_Art_recon.nii.gz")
    tissue_comps = [os.path.join(tissue_dir_path, x) for x in os.listdir(tissue_dir_path)]
    tissue_0_img, tissue_0_arr = get_img_and_arr_from_nii(tissue_comps[0])
    roi_area, slice_thickness = get_area_and_axial_thickness_at_center_L3(roi_img=tissue_0_img, roi_arr=tissue_0_arr, l3_center=center)
    avg_intensity, std_intensity = get_intensity_at_center_L3(ct_arr=ct_arr, roi_arr=tissue_0_arr, l3_center=center)'''

        

