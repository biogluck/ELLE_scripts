import os
import subprocess
import arcpy


DIR = os.getcwd()

for f in os.listdir(DIR):
    if f.endswith("pdf"):
        filename = os.path.basename(f).split('.')[0]
        print(filename)
        out_dir = os.path.join(DIR, filename)
        if not os.path.exists(out_dir):
            os.mkdir(os.path.join(DIR, out_dir))
        subprocess.call(
            ['magick', 'convert', '-density', '300', '-trim', f, os.path.join(out_dir, filename+'.jpg')])
        for jpg_file in os.listdir(out_dir):
            if jpg_file.endswith("jpg"):
                arcpy.DefineProjection_management(
                    in_dataset=os.path.join(out_dir, jpg_file),
                    coor_system="PROJCS['LKS_1992_Latvia_TM',GEOGCS['GCS_LKS_1992',DATUM['D_Latvia_1992',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',-6000000.0],PARAMETER['Central_Meridian',24.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]")
