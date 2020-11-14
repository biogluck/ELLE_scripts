import os
import arcpy


JPG_DIR = os.getcwd()

for f in os.listdir(JPG_DIR):
    if f.endswith("jpg"):
        print('working on ' + f)
        arcpy.DefineProjection_management(
            in_dataset=os.path.join(JPG_DIR, f),
            coor_system="PROJCS['LKS_1992_Latvia_TM',GEOGCS['GCS_LKS_1992',DATUM['D_Latvia_1992',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',-6000000.0],PARAMETER['Central_Meridian',24.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]")
