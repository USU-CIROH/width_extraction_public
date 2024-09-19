import os
import simpledbf
import arcpy
import _thread
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd


# This script is from F:\tuflow-SC\py_modules

def width_series_generator(path_xsect, path_terrains, ini_water_depth, min_elev, max_slope, stop_at_Line_ID,
                           int_len_depth_method, figure_xsect, unit, method, method_width):
    # This python module calculates the flow discharge using the water depth at a certain cross-section
    # The required inputs are:
    #   path_up_xsect         - path to the transect line (XX.shp, shape file)
    #   path_terrain            - path to the terraian (XX.asc)
    #   water_depth             - the water depth at the xsect of interested (e.g. 1st riffle-crest)
    #   figure_xsect            - 1 if you want to see the xsect profile and water stage

    width_series = []

    # path to upstream xsect shp file
    xsectshp1 = path_xsect

    print(xsectshp1)

    # Load Raster DEM
    #terrain = path_terrain

    # Define projection
    dsc = arcpy.Describe(xsectshp1)
    coord_sys = dsc.spatialReference
    #arcpy.DefineProjection_management(terrain, coord_sys)

    terrain_num = 0
    for terrain in path_terrains:
        # Stack Profile
        xsecttab = './gis_files/xsect_table'+str(terrain_num)+'.dbf'
        print(xsecttab)

        if os.path.isfile(xsecttab):
            os.remove(xsecttab)

        # Execute Stack Profile
        arcpy.CheckOutExtension("3D")
        print(os.path.abspath(terrain))
        abspath_terrain = terrain
        arcpy.StackProfile_3d(xsectshp1, profile_targets=[abspath_terrain], out_table=xsecttab)

        if terrain_num == 0: # pre-fire
            xsectdbf0 = simpledbf.Dbf5(xsecttab)
            xsectdfst0 = xsectdbf0.to_dataframe()
            xsectdf0 = xsectdfst0
        elif terrain_num == 1: # post-fire
            xsectdbf1 = simpledbf.Dbf5(xsecttab)
            xsectdfst1 = xsectdbf1.to_dataframe()
            xsectdf1 = xsectdfst1

        #Line_IDs = range(0, max(xsectdf1['LINE_ID'])+1)
        Line_IDs = xsectdf0['LINE_ID'].unique()
        terrain_num += 1

        xsecttable = arcpy.SearchCursor(xsecttab)
        if xsecttable:
            del xsecttable
        # arcpy.management.Delete(xsecttab)

    bed_stage_width_df = pd.DataFrame(np.zeros((max(Line_IDs), len(path_terrains)+3)))
    path_fig = './figures/xsect_' + int_len_depth_method

    for Line_ID in Line_IDs:
        print("Line ID = ", str(Line_ID), ' (or '+str(max(Line_IDs)-Line_ID)+' in figure)')

        x0, z0, width0, min_elevation0, water_stage0, x_intercept0 = width_calculator(xsectdf0, Line_ID,
                                                                                      min_elev,
                                                                                      max_slope, ini_water_depth, method_width)
        x1, z1, width1, min_elevation1, water_stage1, x_intercept1 = width_calculator(xsectdf1, Line_ID,
                                                                                      min_elev,
                                                                                      max_slope, ini_water_depth, method_width)

        if method in ['same_vertical_offset']:

            if figure_xsect == 1:
                # Figure, at the first riffle-crest

                plt.figure(1)
                max_x = np.max([np.max(x0), np.max(x1)])
                plt.plot(max_x-x0, z0, '-', label='pre-fire')
                plt.plot(max_x-[np.min(x0), np.max(x0)], [water_stage0, water_stage0])
                plt.plot(max_x-x_intercept0, water_stage0 * np.ones(len(x_intercept0)), '*')
                plt.plot(max_x-x1, z1, '--', label='post-fire')
                plt.plot(max_x-[np.min(x1), np.max(x1)], [water_stage1, water_stage1])
                plt.plot(max_x-x_intercept1, water_stage1 * np.ones(len(x_intercept1)), '*')
                # plt.plot(xi1, water_stage, 'r*')
                # plt.plot(xi2, water_stage, 'r*')
                """
                plt.figure(1)
                plt.plot(x0, z0, '-', label='pre-fire')
                plt.plot([np.min(x0), np.max(x0)], [water_stage0, water_stage0])
                plt.plot(x_intercept0, water_stage0 * np.ones(len(x_intercept0)), '*')
                plt.plot(x1, z1, '--', label='post-fire')
                plt.plot([np.min(x1), np.max(x1)], [water_stage1, water_stage1])
                plt.plot(x_intercept1, water_stage1 * np.ones(len(x_intercept1)), '*')
                # plt.plot(xi1, water_stage, 'r*')
                # plt.plot(xi2, water_stage, 'r*')
                """
                plt.grid()
                plt.legend()
                plt.xlabel('Lateral Distance ' + '(' + unit + ')')
                plt.ylabel('Elevation ' + '(' + unit + ')')
                plt.title('Cross-sectional profile')
                # plt.show()

                if not os.path.exists(path_fig):
                    os.mkdir(path_fig)

        elif method in ['same_water_stage']:

            if water_stage0 > water_stage1:
                modi_water_depth = water_stage0 - min_elevation1

                x1, z1, width1, min_elevation1, water_stage1, x_intercept1 = width_calculator(xsectdf1, Line_ID,
                                                                                              min_elev,
                                                                                              max_slope,
                                                                                              modi_water_depth, method_width)
            elif water_stage1 > water_stage0:
                modi_water_depth = water_stage1 - min_elevation0
                x0, z0, width0, min_elevation0, water_stage0, x_intercept0 = width_calculator(xsectdf0, Line_ID,
                                                                                              min_elev,
                                                                                              max_slope,
                                                                                              modi_water_depth, method_width)
            if figure_xsect == 1:
                # Figure, at the first riffle-crest
                plt.figure(1)
                max_x = np.max([np.max(x0), np.max(x1)])
                plt.figure(1)
                max_x = np.max([np.max(x0), np.max(x1)])
                plt.plot(max_x-x0, z0, '-', label='pre-fire')
                plt.plot(max_x-[np.min(x0), np.max(x0)], [water_stage0, water_stage0])
                plt.plot(max_x-x_intercept0, water_stage0 * np.ones(len(x_intercept0)), '*')
                plt.plot(max_x-x1, z1, '--', label='post-fire')
                plt.plot(max_x-[np.min(x1), np.max(x1)], [water_stage1, water_stage1])
                plt.plot(max_x-x_intercept1, water_stage1 * np.ones(len(x_intercept1)), '*')
                # plt.plot(xi1, water_stage, 'r*')
                # plt.plot(xi2, water_stage, 'r*')

                plt.grid()
                plt.legend()
                plt.xlabel('Lateral Distance ' + '(' + unit + ')')
                plt.ylabel('Elevation ' + '(' + unit + ')')
                plt.title('Cross-sectional profile')
                # plt.show()

                if not os.path.exists(path_fig):
                    os.mkdir(path_fig)


        #width_series = np.append(width_series, width)
        bed_stage_width_df.loc[max(Line_IDs) - Line_ID, 0] = min_elevation0
        bed_stage_width_df.loc[max(Line_IDs) - Line_ID, 1] = min_elevation1
        bed_stage_width_df.loc[max(Line_IDs) - Line_ID, 2] = water_stage0
        bed_stage_width_df.loc[max(Line_IDs) - Line_ID, 3] = width0
        bed_stage_width_df.loc[max(Line_IDs) - Line_ID, 4] = width1
#comment out block below here to toggle on/off certain station figure for figures
        if figure_xsect == 1:
            plt.savefig(path_fig + '/profile_' + str(max(Line_IDs) - Line_ID))

            if max(Line_IDs) - Line_ID == stop_at_Line_ID:
                #os.system("pause")
                break
            plt.close()
        plt.close('all')


    return Line_IDs, bed_stage_width_df

def width_calculator(xsectdf1, Line_ID, min_elev, max_slope, water_depth, method_width):
    # Construct a functional relationship between A and h
    x = np.array(xsectdf1.loc[xsectdf1['LINE_ID'] == Line_ID]['FIRST_DIST'])
    z = np.array(xsectdf1.loc[xsectdf1['LINE_ID'] == Line_ID]['FIRST_Z'])

    ind_nan = np.where(z < min_elev)  # z == -9999
    x = np.delete(x, ind_nan)
    z = np.delete(z, ind_nan)

    slope = np.diff(z)/np.diff(x)
    ind_diff = np.where(slope > max_slope)

    if len(ind_diff[0]) > 0:
        x = np.delete(x, ind_diff[0])
        z = np.delete(z, ind_diff[0])
        if ind_diff[0][0] > 0:
            x = np.delete(x, range(ind_diff[0][0])) # delete the left part of the profile as well
            z = np.delete(z, range(ind_diff[0][0]))

    slope = np.diff(z) / np.diff(x)
    ind_diff = np.where(slope < -max_slope)
    if len(ind_diff[0]) > 0:
        x = np.delete(x, ind_diff[0] + 1)
        z = np.delete(z, ind_diff[0] + 1)

    min_elevation = min(z)  # np.sort(z)[1]

    water_stage = min_elevation + water_depth

    z0 = z - water_stage
    # print(z0)
    ind = []
    x_intercept = []

    # Calculate Width

    for ii in range(0, z.__len__() - 1):
        if np.sign(z0[ii] * z0[ii + 1]) < 0:
            ind.append(ii)

    width = 0

    """    
    ## width = distance between the first & last intersect w/ water stage
    for ii in range(0, ind.__len__()):
        if len(ind) > 1:

            m1 = (z0[ind[ii]] - z0[ind[ii] + 1]) / (x[ind[ii]] - x[ind[ii] + 1])
            xi1 = (-z0[ind[ii]] + m1 * x[ind[ii]]) / m1

            x_intercept = np.append(x_intercept, xi1)

            width = x_intercept[-1] - x_intercept[0]

        else:
            width = 0
    """

    ## width = summation of distances between the intersect w/ water stage
    for ii in range(0, ind.__len__(), 2):
        if len(ind) > 1:

            m1 = (z0[ind[ii]] - z0[ind[ii] + 1]) / (x[ind[ii]] - x[ind[ii] + 1])
            xi1 = (-z0[ind[ii]] + m1 * x[ind[ii]]) / m1

            m2 = (z0[ind[ii+1]] - z0[ind[ii+1] + 1]) / (x[ind[ii+1]] - x[ind[ii+1] + 1])
            xi2 = (-z0[ind[ii+1]] + m2 * x[ind[ii+1]]) / m2

            dx = xi2 - xi1

            width = width + dx

            x_intercept = np.append(x_intercept, xi1)
            x_intercept = np.append(x_intercept, xi2)

        else:
            width = 0

    if method_width in ['total']:
        if width > 0:
            width = x_intercept[-1] - x_intercept[0]
            x_intercept = [x_intercept[0], x_intercept[-1]]
    # else:
    #     print("method_width = sum")

    return x, z, width, min_elevation, water_stage, x_intercept