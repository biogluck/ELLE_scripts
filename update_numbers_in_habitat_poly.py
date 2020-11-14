import os
import csv
import arcpy

def get_experts(csv_file):
    experts = {}
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f, delimiter='\t') 
        next(csv_reader)
        for line in csv_reader:
            experts[line[0]] = line[1]
    return experts



WORKDIR = os.getcwd()
# experts.csv should have name in 1st column and code in 2nd
experts_file = os.path.join(WORKDIR, 'experts.csv')

experts = get_experts(experts_file)


def update_numbers(fc):
    cursor = arcpy.UpdateCursor(fc)
    for row in cursor:
        form_number = row.getValue("FORM_NUMBER")
        if row.getValue("OBSERVER"):
            expert_name = row.getValue("OBSERVER").encode("utf-8")
        polygon_number = row.getValue("POLYGON_NUMBER")
        not_ec = row.getValue("NOT_EC")
        if expert_name:
            expert_code = experts.get(expert_name)
        if not polygon_number:
            print "no poly number"
            return
        if polygon_number.isdigit():
            print "setting new polygon number"
            new_polygon_number = expert_code + "_" + str(polygon_number)
            row.setValue("POLYGON_NUMBER", new_polygon_number)
            cursor.updateRow(row)
        if form_number:
            if form_number.count("_") == 1:
                # if has form_number without expert prefix
                new_form_number = expert_code + "_" + form_number
                row.setValue("FORM_NUMBER", new_form_number)
                cursor.updateRow(row)   
        else:
            if polygon_number and polygon_number.isdigit() and not not_ec:
                new_form_number = expert_code + '_' + polygon_number + '_1'
                row.setValue("FORM_NUMBER", new_form_number)
                cursor.updateRow(row)



for path in os.listdir(WORKDIR):
    if path.endswith('.gdb'):
        fc = os.path.join(WORKDIR, path )+ "\Habitat_poly"
        print 'Updating numbers for {}'.format(fc)
        update_numbers(fc)
        print "="*70
