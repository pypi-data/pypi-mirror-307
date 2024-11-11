import os
import numpy as np
import SimpleITK as sitk

# Method 1) Volume percentage changes
def get_volume_perc_of_roi(roi_area, body_cav_area):
    roi_perc = round(roi_area / body_cav_area * 100, 4)
    return roi_perc

def perc_volPerc_diff(roi_perc_T0, roi_perc_T1):
    perc_diff = round((roi_perc_T1 - roi_perc_T0) / roi_perc_T0 * 100, 4)
    return perc_diff

def rate_perc_volPerc_diff(roi_perc_T0, roi_perc_T1, time_interval):
    perc_diff = perc_volPerc_diff(roi_perc_T0, roi_perc_T1)
    rate_perc_diff = round(perc_diff / time_interval, 4)
    return rate_perc_diff

# Method 2) Surface area changes & Method 3) Intensity changes
def perc_area_diff(val_T0, val_T1):
    perc_diff = round((val_T1 - val_T0) / val_T0 * 100, 4)
    return perc_diff

def rate_perc_area_diff(val_T0, val_T1, time_interval):
    perc_diff = perc_area_diff(val_T0=val_T0, val_T1=val_T1)
    rate_perc_diff = round(perc_diff / time_interval, 4)
    return rate_perc_diff

if __name__ == "__main__":
    pass







