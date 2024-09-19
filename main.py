import os
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from width_series_generator import *

## width_extraction python codes
##      developed by Anzy Lee, Utah State University

## Inputs
#   path_xsect         - path to the transect lines
#                       (e.g., './gis_files/LP_20220819_STAlines_5m_200m.shp' where station interval = 5 m, length = 200 m)
#   path_terrains       - path to the terraian (XX.asc), can process two terrains as of now
#                       (e.g., ['./DEM/merged_2016_220510_Clip.tif', './DEM/Sanborn_2021_1m_merged_HUC1.tif'])

## Output
#   Figures of XS profiles of multiple terrains in 'figures' folder
#   Figures of longitudinal bed elevation and width series in 'figures' folder
#   Table of longitudinal bed elevation and width series in 'tables' folder

## Example code
#   This example extracts XS profiles from a pre-fire and post-fire terrains, calcualtes widths, and and see how they change.

## Variables
thalweg_name = 'thalweg'        # name of thalweg shape file (used for path_xsect)
interval = 20                    # interval of XS lines in meter
station_length = 200            # length of XS lines (used for path_xsect)
is_x_from_upstream = 0          # 1 if XS line starts from upstream, 0 if from downstreasm

## Methods and parameters
method = 'same_vertical_offset'     # 'same_vertical_offset' or 'same_water_stage'
water_depth = 1.25                  # the water depth at the xsect of interested (e.g. 1st riffle-crest)

#################################################################

## Other parameters (default)
stop_at_Line_ID = np.nan        # Line ID of XS that stops width extraction (used for path_xsect)
method_width = 'sum'            # 'sum': summation of fractions of widths (default), 'total': from the far left to far right ,
min_elev = 1000                 # Default elevation added to DEM
max_slope = 20                  # Upper limit of imaginary WSE slope
figure_xsect = 1                # 1 to save figure, 0 to only produce numbers/tables

water_depth_str = "%.2f" % water_depth
water_depth_str = water_depth_str.replace('.','p')

int_len = str(interval)+'m_'+str(station_length)+'m'
int_len_depth_method = str(interval)+'m_'+str(station_length)+'m_'+water_depth_str+'m_'+method

path_xsect = './gis_files/'+thalweg_name+'_XS_'+int_len+'.shp'
path_terrains = ['./DEM/pre-fire.tif', './DEM/post-fire.tif'] # [pre-fire, post-fire]

unit = 'SI'

Line_IDs_orig, bed_stage_width_df_orig = width_series_generator(path_xsect, path_terrains, water_depth, min_elev, max_slope, stop_at_Line_ID,
                                                int_len_depth_method, figure_xsect, unit, method, method_width)

if stop_at_Line_ID > 0:
    if is_x_from_upstream == 0:
        Line_IDs = Line_IDs_orig[stop_at_Line_ID:]
        bed_stage_width_df = bed_stage_width_df_orig[stop_at_Line_ID:]
    else:
        Line_IDs = Line_IDs_orig[:stop_at_Line_ID+1]
        bed_stage_width_df = bed_stage_width_df_orig[:stop_at_Line_ID+1]
else:
    Line_IDs = Line_IDs_orig
    bed_stage_width_df = bed_stage_width_df_orig

x_dist = Line_IDs*interval

#if is_x_from_upstream == 0:
#    x_dist_from_upstream = max(x_dist) - x_dist
#else:
#    x_dist_from_upstream = x_dist

plt.figure(figsize=(12,6))
plt.plot(x_dist, bed_stage_width_df.iloc[:, 3], label='Pre-fire width')
plt.plot(x_dist, bed_stage_width_df.iloc[:, 4], label='Post-fire width')
plt.xlabel('Longitudinal distance (m)')
plt.ylabel('Width series at depth = '+ str(water_depth) +' m (m)')
plt.legend()
plt.savefig('./figures/w_series_'+int_len_depth_method)

plt.figure(figsize=(12,6))
plt.plot(x_dist, bed_stage_width_df.iloc[:, 0], '-', label='Pre-fire profile')
plt.plot(x_dist, bed_stage_width_df.iloc[:, 1], '--', label='Post-fire profile')
plt.plot(x_dist, bed_stage_width_df.iloc[:, 2], '-', label='Water stage')
plt.xlabel('Longitudinal distance (m)')
plt.ylabel('Thalweg bed profile and water stage (m)')
plt.legend()
plt.savefig('./figures/z_series_'+int_len_depth_method)

path_xlsx = './tables/width_'+int_len_depth_method+'.xlsx'
tmp = np.transpose(np.array([x_dist]))
tmp_stack = np.hstack([tmp, bed_stage_width_df])
df = pd.DataFrame(data=tmp_stack, columns=['x_dist',
                                           'pre_bed_profile', 'post_bed_profile', 'water_stage',
                                           'width_pre', 'width_post'])
df.to_excel(path_xlsx)

terrain_num = 0
for terrain in path_terrains:
    xsecttab = './gis_files/xsect_table' + str(terrain_num) + '.dbf'
    arcpy.management.Delete(xsecttab)
    terrain_num += 1
