import os
import numpy as np
import pandas as pd
from body_composition.utils import dicom2nifti, run_total_segmentator, vol_and_int_extraction, calculate_changes


class DataProcessor:
    def __init__(self, Patient_Identifier, dicom_path_T0:str, dicom_path_T1:str, time_interval:int, save_file:str, verbose = 1):
        if self.check_initial_requirements(dicom_path_T0) and self.check_initial_requirements(dicom_path_T1):
            self.Patient_Identifier = str(Patient_Identifier)
            self.dicom_path_T0 = dicom_path_T0
            self.dicom_path_T1 = dicom_path_T1
            self.time_interval = time_interval
            self.save_file = save_file
            self.verbose = verbose

        # Run module one by one. 
        self.module_01_convert_to_niftis()
        self.module_02_run_total_setmentator()
        self.module_03_extract_metrics()
        self.module_04_calculate_changes()
        self.module_05_save_outputs()

    def check_initial_requirements(self, dicom_path):
        if not os.path.isdir(dicom_path):
            raise ValueError(f"{dicom_path} is not a valid directory.")
        else:
            if not any(fname.endswith('.dcm') for fname in os.listdir(dicom_path)):
                raise ValueError(f"{dicom_path} has no dicom file.")
            else:
                return True

    def module_01_convert_to_niftis(self):
        self.nii_path_T0 = os.path.join(os.path.dirname(self.dicom_path_T0), os.path.basename(self.dicom_path_T0)+".nii.gz")
        self.nii_path_T1 = os.path.join(os.path.dirname(self.dicom_path_T1), os.path.basename(self.dicom_path_T1)+".nii.gz")
        dicom2nifti.dicom2nifti(self.dicom_path_T0, self.nii_path_T0, verbose=self.verbose)
        dicom2nifti.dicom2nifti(self.dicom_path_T1, self.nii_path_T1, verbose=self.verbose)

    def module_02_run_total_setmentator(self):
        self.total_seg_dir_path_T0, self.tissue_seg_dir_path_T0, self.body_seg_dir_path_T0 = run_total_segmentator.run_segmentator_for_body_comp(self.nii_path_T0, verbose=self.verbose)
        self.total_seg_dir_path_T1, self.tissue_seg_dir_path_T1, self.body_seg_dir_path_T1 = run_total_segmentator.run_segmentator_for_body_comp(self.nii_path_T1, verbose=self.verbose)
        
    def module_03_extract_metrics(self):
        # Prepare CT img and arr.
        self.ct_img_T0, self.ct_arr_T0 = vol_and_int_extraction.get_img_and_arr_from_nii(self.nii_path_T0)
        self.ct_img_T1, self.ct_arr_T1 = vol_and_int_extraction.get_img_and_arr_from_nii(self.nii_path_T1)

        self.module_03_organ_vol_and_intsty_extraction()
        self.module_03_tissue_vol_and_intsty_extraction()

    def module_03_organ_vol_and_intsty_extraction(self):
        def get_vol_and_intensity(roi_nii_path, ct_arr):
            roi_img, roi_arr = vol_and_int_extraction.get_img_and_arr_from_nii(nii_path= roi_nii_path)
            roi_vol, roi_is_truncated = vol_and_int_extraction.get_volume_from_mask_nii(roi_img, roi_arr)
            roi_avg_intensity, roi_std_intensity = vol_and_int_extraction.get_intensity(ct_arr, roi_arr)
            return (roi_vol, roi_is_truncated, roi_avg_intensity, roi_std_intensity)
        
        # Liver, Pancreas
        # T0: ex. baseline
        self.liver_nii_path_T0 = os.path.join(self.total_seg_dir_path_T0, "liver.nii.gz")
        self.liver_vol_T0, self.liver_is_truncated_T0, self.liver_avg_intensity_T0, self.liver_std_intensity_T0 = get_vol_and_intensity(roi_nii_path=self.liver_nii_path_T0, ct_arr=self.ct_arr_T0)
        self.pancreas_nii_path_T0 = os.path.join(self.total_seg_dir_path_T0, "pancreas.nii.gz")
        self.pancreas_vol_T0, self.pancreas_is_truncated_T0, self.pancreas_avg_intensity_T0, self.pancreas_std_intensity_T0 = get_vol_and_intensity(roi_nii_path=self.pancreas_nii_path_T0, ct_arr=self.ct_arr_T0)
        
        # T1: ex. pre-surgery
        self.liver_nii_path_T1 = os.path.join(self.total_seg_dir_path_T1, "liver.nii.gz")
        self.liver_vol_T1, self.liver_is_truncated_T1, self.liver_avg_intensity_T1, self.liver_std_intensity_T1 = get_vol_and_intensity(roi_nii_path=self.liver_nii_path_T1, ct_arr=self.ct_arr_T1)
        self.pancreas_nii_path_T1 = os.path.join(self.total_seg_dir_path_T1, "pancreas.nii.gz")
        self.pancreas_vol_T1, self.pancreas_is_truncated_T1, self.pancreas_avg_intensity_T1, self.pancreas_std_intensity_T1 = get_vol_and_intensity(roi_nii_path=self.pancreas_nii_path_T1, ct_arr=self.ct_arr_T1)
        
    def module_03_tissue_vol_and_intsty_extraction(self):
        def get_area_and_intensity_at_l3_center(tissue_nii_path, ct_arr, l3_center):
            tissue_img, tissue_arr = vol_and_int_extraction.get_img_and_arr_from_nii(tissue_nii_path)
            tissue_area, slice_thickness = vol_and_int_extraction.get_area_and_axial_thickness_at_center_L3(roi_img =tissue_img, roi_arr = tissue_arr, l3_center=l3_center)
            tissue_avg_intensity, tissue_std_intensity = vol_and_int_extraction.get_intensity_at_center_L3(ct_arr = ct_arr, roi_arr = tissue_arr, l3_center = l3_center)
            return (tissue_area, slice_thickness, tissue_avg_intensity, tissue_std_intensity)
        
        # Visceral adbominal fat (VAF), Subcutaneous abdominal fat (SAF), Skeletal muscle area (SMA)
        # T0: ex. baseline
        _, self.L3_center_T0, _, self.note_T0 = vol_and_int_extraction.get_center_L3(self.total_seg_dir_path_T0)
        self.VAF_area_T0, self.slice_thickness_T0, self.VAF_avg_intensity_T0, self.VAF_std_intensity_T0 = get_area_and_intensity_at_l3_center(tissue_nii_path=os.path.join(self.tissue_seg_dir_path_T0, "torso_fat.nii.gz"), ct_arr=self.ct_arr_T0, l3_center=self.L3_center_T0)
        self.SAF_area_T0, _, self.SAF_avg_intensity_T0, self.SAF_std_intensity_T0 = get_area_and_intensity_at_l3_center(tissue_nii_path=os.path.join(self.tissue_seg_dir_path_T0, "subcutaneous_fat.nii.gz"), ct_arr=self.ct_arr_T0, l3_center=self.L3_center_T0)
        self.SMA_area_T0, _, self.SMA_avg_intensity_T0, self.SMA_std_intensity_T0 = get_area_and_intensity_at_l3_center(tissue_nii_path=os.path.join(self.tissue_seg_dir_path_T0, "skeletal_muscle.nii.gz"), ct_arr=self.ct_arr_T0, l3_center=self.L3_center_T0)
        # T1: ex. pre-surgery
        _, self.L3_center_T1, _, self.note_T1 = vol_and_int_extraction.get_center_L3(self.total_seg_dir_path_T1)
        self.VAF_area_T1, self.slice_thickness_T1, self.VAF_avg_intensity_T1, self.VAF_std_intensity_T1 = get_area_and_intensity_at_l3_center(tissue_nii_path=os.path.join(self.tissue_seg_dir_path_T1, "torso_fat.nii.gz"), ct_arr=self.ct_arr_T1, l3_center=self.L3_center_T1)
        self.SAF_area_T1, _, self.SAF_avg_intensity_T1, self.SAF_std_intensity_T1 = get_area_and_intensity_at_l3_center(tissue_nii_path=os.path.join(self.tissue_seg_dir_path_T1, "subcutaneous_fat.nii.gz"), ct_arr=self.ct_arr_T1, l3_center=self.L3_center_T1)
        self.SMA_area_T1, _, self.SMA_avg_intensity_T1, self.SMA_std_intensity_T1 = get_area_and_intensity_at_l3_center(tissue_nii_path=os.path.join(self.tissue_seg_dir_path_T1, "skeletal_muscle.nii.gz"), ct_arr=self.ct_arr_T1, l3_center=self.L3_center_T1)
        
    def module_04_calculate_changes(self):
        # Prepare body cavity arr.
        self.body_cav_img_T0, self.body_cav_arr_T0 = vol_and_int_extraction.get_img_and_arr_from_nii(nii_path=os.path.join(self.body_seg_dir_path_T0, "body.nii.gz"))
        self.body_cav_arr_T0, _ = vol_and_int_extraction.get_area_and_axial_thickness_at_center_L3(self.body_cav_img_T0 , self.body_cav_arr_T0, self.L3_center_T0) # at center L3
        self.body_cav_img_T1, self.body_cav_arr_T1 = vol_and_int_extraction.get_img_and_arr_from_nii(nii_path=os.path.join(self.body_seg_dir_path_T1, "body.nii.gz"))
        self.body_cav_arr_T1, _ = vol_and_int_extraction.get_area_and_axial_thickness_at_center_L3(self.body_cav_img_T1 , self.body_cav_arr_T1, self.L3_center_T1) # at center L3
        
        self.module_04_organ_changes()
        self.module_04_tissue_changes()
    
    def module_04_organ_changes(self):
        def get_organ_changes(vol_T0, vol_T1, time_interval, is_truncated:bool):
            if not is_truncated:
                perc_diff = calculate_changes.perc_volPerc_diff(roi_perc_T0 = vol_T0, roi_perc_T1 = vol_T1)
                rate_perc_diff = calculate_changes.rate_perc_volPerc_diff(roi_perc_T0=vol_T0, roi_perc_T1=vol_T1, time_interval=time_interval)
                return (perc_diff, rate_perc_diff)
            else:
                return (None, None)
        # Liver, Pancreas
        self.liver_changes_vol_perc, self.liver_changes_vol_perc_rate = get_organ_changes(self.liver_vol_T0, self.liver_vol_T1, time_interval=self.time_interval, is_truncated=self.liver_is_truncated_T0 or self.liver_is_truncated_T1)
        self.pancreas_changes_vol_perc, self.pancreas_changes_vol_perc_rate = get_organ_changes(self.pancreas_vol_T0, self.pancreas_vol_T1, time_interval=self.time_interval, is_truncated=self.pancreas_is_truncated_T0 or self.pancreas_is_truncated_T1)
        #print(self.liver_changes_vol_perc, self.liver_changes_vol_perc_rate,  self.pancreas_changes_vol_perc, self.pancreas_changes_vol_perc_rate)

    def module_04_tissue_changes(self):
        def get_tissue_changes(tissue_area_T0, tissue_area_T1, body_cav_arr_T0, body_cav_arr_T1, tissue_avg_intensity_T0, tissue_avg_intensity_T1, time_interval):
            tissue_vol_perc_T0 = calculate_changes.get_volume_perc_of_roi(tissue_area_T0, body_cav_arr_T0)
            tissue_vol_perc_T1 = calculate_changes.get_volume_perc_of_roi(tissue_area_T1, body_cav_arr_T1)
            tissue_changes_vol_perc = calculate_changes.perc_volPerc_diff(roi_perc_T0=tissue_vol_perc_T0, roi_perc_T1=tissue_vol_perc_T1) # Method 1-1. Volume percentage diff.
            tissue_changes_vol_perc_rate = calculate_changes.rate_perc_volPerc_diff(roi_perc_T0=tissue_vol_perc_T0, roi_perc_T1=tissue_vol_perc_T1, time_interval=time_interval) # Method 1-2. Volume percentage diff. per time

            tissue_changes_surf_area = calculate_changes.perc_area_diff(val_T0=tissue_area_T0, val_T1=tissue_area_T1) # Method 2-1. Surface area diff.
            tissue_changes_surf_area_rate = calculate_changes.rate_perc_area_diff(val_T0=tissue_area_T0, val_T1=tissue_area_T1, time_interval=time_interval) # Method 2-2. Surface area diff. per time

            tissue_changes_intensity = calculate_changes.perc_area_diff(val_T0=tissue_avg_intensity_T0, val_T1=tissue_avg_intensity_T1) # Method 3-1. Avg. intensity diff
            tissue_changes_intensity_rate = calculate_changes.rate_perc_area_diff(val_T0=tissue_avg_intensity_T0, val_T1=tissue_avg_intensity_T1, time_interval=time_interval) # Method 3-2. Avg. intensity diff. per time
            return (tissue_changes_vol_perc, tissue_changes_vol_perc_rate, tissue_changes_surf_area, tissue_changes_surf_area_rate, tissue_changes_intensity, tissue_changes_intensity_rate)

        # Visceral adbominal fat (VAF), Subcutaneous abdominal fat (SAF), Skeletal muscle area (SMA)
        self.VAF_changes_vol_perc, self.VAF_changes_vol_perc_rate, self.VAF_changes_surf_area, self.VAF_changes_surf_area_rate, self.VAF_changes_intensity, self.VAF_changes_intensity_rate \
                = get_tissue_changes(tissue_area_T0=self.VAF_area_T0, tissue_area_T1=self.VAF_area_T1, body_cav_arr_T0=self.body_cav_arr_T0, body_cav_arr_T1=self.body_cav_arr_T1,
                                     tissue_avg_intensity_T0=self.VAF_avg_intensity_T0, tissue_avg_intensity_T1=self.VAF_avg_intensity_T1, time_interval=self.time_interval)
        self.SAF_changes_vol_perc, self.SAF_changes_vol_perc_rate, self.SAF_changes_surf_area, self.SAF_changes_surf_area_rate, self.SAF_changes_intensity, self.SAF_changes_intensity_rate \
                = get_tissue_changes(tissue_area_T0=self.SAF_area_T0, tissue_area_T1=self.SAF_area_T1, body_cav_arr_T0=self.body_cav_arr_T0, body_cav_arr_T1=self.body_cav_arr_T1,
                                     tissue_avg_intensity_T0=self.SAF_avg_intensity_T0, tissue_avg_intensity_T1=self.SAF_avg_intensity_T1, time_interval=self.time_interval)
        self.SMA_changes_vol_perc, self.SMA_changes_vol_perc_rate, self.SMA_changes_surf_area, self.SMA_changes_surf_area_rate, self.SMA_changes_intensity, self.SMA_changes_intensity_rate \
                = get_tissue_changes(tissue_area_T0=self.SMA_area_T0, tissue_area_T1=self.SMA_area_T1, body_cav_arr_T0=self.body_cav_arr_T0, body_cav_arr_T1=self.body_cav_arr_T1,
                                     tissue_avg_intensity_T0=self.SMA_avg_intensity_T0, tissue_avg_intensity_T1=self.SMA_avg_intensity_T1, time_interval=self.time_interval)
        #print(self.VAF_changes_vol_perc, self.VAF_changes_vol_perc_rate, self.VAF_changes_surf_area, self.VAF_changes_surf_area_rate, self.VAF_changes_intensity, self.VAF_changes_intensity_rate )         

    def module_05_group_by_loss_and_gain(self):
        def loss_or_gain(change_value):
            if change_value is None:
                return None
            else:
                return 'gain' if change_value > 0 else 'loss'
        
        self.liver_loss_or_gain = loss_or_gain(self.liver_changes_vol_perc)
        self.pancreas_loss_or_gain = loss_or_gain(self.pancreas_changes_vol_perc)

        self.VAF_vol_perc_loss_or_gain = loss_or_gain(self.VAF_changes_vol_perc)
        self.VAF_surf_area_loss_or_gain = loss_or_gain(self.VAF_changes_surf_area)
        self.VAF_intensity_loss_or_gain = loss_or_gain(self.VAF_changes_intensity)

        self.SAF_vol_perc_loss_or_gain = loss_or_gain(self.SAF_changes_vol_perc)
        self.SAF_surf_area_loss_or_gain = loss_or_gain(self.SAF_changes_surf_area)
        self.SAF_intensity_loss_or_gain = loss_or_gain(self.SAF_changes_intensity)

        self.SMA_vol_perc_loss_or_gain = loss_or_gain(self.SMA_changes_vol_perc)
        self.SMA_surf_area_loss_or_gain = loss_or_gain(self.SMA_changes_surf_area)
        self.SMA_intensity_loss_or_gain = loss_or_gain(self.SMA_changes_intensity)
    
    def module_05_save_outputs(self):
        self.module_05_group_by_loss_and_gain()
        
        keys = [ 'Patient_Identifier', 
                
                # T0: ex. baseline
                'liver_vol_T0', 'liver_is_truncated_T0', 'liver_avg_intensity_T0', 'liver_std_intensity_T0',  # liver
                'pancreas_vol_T0', 'pancreas_is_truncated_T0', 'pancreas_avg_intensity_T0', 'pancreas_std_intensity_T0', # pancreas
                'VAF_area_T0', 'VAF_avg_intensity_T0', 'VAF_std_intensity_T0', # Visceral abdominal fat (VAF)
                'SAF_area_T0', 'SAF_avg_intensity_T0', 'SAF_std_intensity_T0', # Subcutaneous abdominal fat (SAF)
                'SMA_area_T0', 'SMA_avg_intensity_T0', 'SMA_std_intensity_T0', # Skeletal muscle area (SMA)
                'slice_thickness_T0', # slice thickness
                '   ',
                # T1: ex. pre-surgery
                'liver_vol_T1', 'liver_is_truncated_T1', 'liver_avg_intensity_T1', 'liver_std_intensity_T1', # liver
                'pancreas_vol_T1', 'pancreas_is_truncated_T1', 'pancreas_avg_intensity_T1', 'pancreas_std_intensity_T1', # pancreas
                'VAF_area_T1', 'VAF_avg_intensity_T1', 'VAF_std_intensity_T1', # Visceral abdominal fat (VAF)
                'SAF_area_T1', 'SAF_avg_intensity_T1', 'SAF_std_intensity_T1', # Subcutaneous abdominal fat (SAF)
                'SMA_area_T1', 'SMA_avg_intensity_T1', 'SMA_std_intensity_T1', # Skeletal muscle area (SMA)
                'slice_thickness_T1', # slice thickness
                '   ',
                # Changes between T0 and T1
                'liver_changes_vol_perc', 'liver_changes_vol_perc_rate', # liver
                'pancreas_changes_vol_perc', 'pancreas_changes_vol_perc_rate', # pancreas
                'VAF_changes_vol_perc', 'VAF_changes_vol_perc_rate', 'VAF_changes_surf_area', 'VAF_changes_surf_area_rate', 'VAF_changes_intensity', 'VAF_changes_intensity_rate', # Visceral abdominal fat (VAF)
                'SAF_changes_vol_perc', 'SAF_changes_vol_perc_rate', 'SAF_changes_surf_area', 'SAF_changes_surf_area_rate', 'SAF_changes_intensity', 'SAF_changes_intensity_rate', # Subcutaneous abdominal fat (SAF)
                'SMA_changes_vol_perc', 'SMA_changes_vol_perc_rate', 'SMA_changes_surf_area', 'SMA_changes_surf_area_rate', 'SMA_changes_intensity', 'SMA_changes_intensity_rate', # Skeletal muscle area (SMA)
                '   ',
                ## Group by loss or gain 
                'liver_loss_or_gain', 'pancreas_loss_or_gain', # liver, pancreas
                'VAF_vol_perc_loss_or_gain', 'VAF_surf_area_loss_or_gain', 'VAF_intensity_loss_or_gain', # Visceral abdominal fat (VAF)
                'SAF_vol_perc_loss_or_gain', 'SAF_surf_area_loss_or_gain', 'SAF_intensity_loss_or_gain', # Subcutaneous abdominal fat (SAF)
                'SMA_vol_perc_loss_or_gain', 'SMA_surf_area_loss_or_gain', 'SMA_intensity_loss_or_gain' # Skeletal muscle area (SMA)
                ]
        

        self.output_df = pd.DataFrame([{key: getattr(self, key, None) for key in keys}])
        self.output_df.to_csv(self.save_file, index=False)


if __name__ == "__main__":
    # Input: a pair of dicom series directory, time stamp (if not inside the meta data)
    # Output: excel sheet with one row, center of L3 with colored tissue masks, Loss of 
    dir_path = "/Radonc/Cancer Physics and Engineering Lab/Yeseul Kim/Important_Dataset/MDACC/Converted_NIFTIs/Complete/Only_L3Center/456182/Validated_BL_and_PreSurg"
    dicom_path_T0 = os.path.join(dir_path, "BL_CTScans", "Art_recon")
    dicom_path_T1 = os.path.join(dir_path, "PreSurg_CTScans", "Art_raw")
    save_file = os.path.join(dir_path, "sample_output.csv")

    DataProcessor(Patient_Identifier = 456182, dicom_path_T0=dicom_path_T0, dicom_path_T1=dicom_path_T1, time_interval=90, save_file = save_file, verbose = 0)







