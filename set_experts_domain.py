# coding: utf8
import arcpy
import csv
import os


WORKDIR = os.getcwd()
experts = []

with open(os.path.join(WORKDIR, 'experts.csv'), 'r') as f:
    csv_reader = csv.reader(f, delimiter='\t')
    next(csv_reader)
    for line in csv_reader:
        print(line)
        experts.append(line[0])

for gdb in os.listdir(WORKDIR):
    if gdb.endswith('.gdb'):
        print('found ' + gdb)
        for expert in experts:
            print ('adding ' + expert)
            arcpy.AddCodedValueToDomain_management(
                in_workspace=os.path.join(WORKDIR, gdb),
                domain_name="experts",
                code=expert,
                code_description=expert)
