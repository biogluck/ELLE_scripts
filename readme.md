# Useful scripts for digitising maps for EU habitats mapping project

Most of these scripts were created for work in ArcGIS Desktop environment. You should use ArcGIS python interpreuter (e.g. C:\Python27\ArcGIS10.5\python.exe).



## 1. `pdf_to_jpeg.cmd`

Script for converting multipage pdf to jpg files.

Requires [ImageMagick](https://imagemagick.org/) to be installed.

Change `input.pdf` and `output.jpg` before run.

Example:

``` cmd
magick convert -density 300 -trim 4511_4_kartes_darba.pdf 4511_4.jpg
```

---

## 2. `assign_projection.py`

Use this script to assign 'LKS_1992_Latvia_TM' projection to all *.jpg files in directory.  

Copy `assign_proj.bat` and `assign_projection.py` files into directory with *.jpg files and run assign_proj.bat.

If your python interpreter location is different from 'C:\Python27\ArcGIS10.5\python.exe', change this in 'assign_proj.bat'.

Or just run
``` cmd
C:\Python27\ArcGIS10.5\python.exe "assign_projection.py"
```

---

## 3. `pdf_to_geojpg.py`

Combination of  `pdf_to_jpeg.cmd` and `assign_projection.py`

* Converts all `.pdf` files in folder to `jpg`
* Creates new folder for new `jpg` files
* Assigns 'LKS_1992_Latvia_TM' projection to all `jpg` files in created folders

Run
``` cmd
C:\Python27\ArcGIS10.5\python.exe "pdf_to_geojpg.py"
```
in folder with `.pdf` maps.


If You need to rename output rasters, the best place where You can do it is ArcGIS Catalog.

---

## 4. `set_experts_domain.py`

Adds expert names to domain 'experts' to all File Geodatabases in folder where You run this script.

To use benefits of this script You should:
- create coded domain 'experts' in .gdb with string data type
- create file `experts.csv` in folder where You run the script. File `experts.csv` is tab-separated `csv` with header, expert names in 1st column and expert codes in 2nd column

Example of `experts.csv`
<table>
<th>
<tr><th>name</th><th>code</th></tr>
</th>
<tbody>
<tr><td>Siarhei Uhlianets</td><td>20SU869</td></tr>
<tr><td>Donald Trump</td><td>20DT000</td></tr>
</tbody>
</table>

Run
``` cmd
C:\Python27\ArcGIS10.5\python.exe "set_experts_domain.py"
```
in folder with `.gdb` folder(s).

---

## 5. `update_fields.py`

Updates `"FORM_NUMBER"` and `"POLYGON_NUMBER"` fields in `Habitat_poly` Feature Class in every `.gdb` in directory where You run this script.

Requires `experts.csv` with correct names and codes of experts.

The script:

* calculates `EC_NAME` for records with `CODE_EC`
* if `"POLYGON_NUMBER"` is number (e.g. `42`), corrects `"POLYGON_NUMBER"` to `XXYYZZZ_42`, where `XXYYZZZ` is experts code
* for features without `"FORM_NUMBER"` if polygon is not `NOT_EC` generates `"FORM_NUMBER"` using `"POLYGON_NUMBER"`
* generates "experts prefix" for `"FORM_NUMBER"` without "experts prefix" 

Run
``` cmd
C:\Python27\ArcGIS10.5\python.exe "update_numbers_in_habitat_poly.py"
```
in folder with `.gdb` folder(s).

---

## 6. `validate.py`

Validates data in `Habitat_poly` Feature Class.

Checks validity of fields "CODE_EC", "NOT_EC", "OBS_DATE", "OBSERVER", "POLYGON_NUMBER", "FORM_NUMBER", "PERCENTAGE_EC", "PERCENTAGE_EC2", "PERCENTAGE_EC3", "PERCENTAGE_NOT_EC". Writes results to `validate.log`.

Requires file `experts.csv` with correct names and codes of experts.

To validate specific geodatabase(s) run:
``` cmd
C:\Python27\ArcGIS10.5\python.exe validate.py gdb1.gdb gdb2.gdb ...
```

To validate all geodatabases in directory run without command line arguments:
``` cmd
C:\Python27\ArcGIS10.5\python.exe validate.py
```

Then check `validate.log` and correct mistakes.