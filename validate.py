# -*- coding: utf-8 -*-
# C:\Python27\ArcGIS10.5\python.exe

import arcpy
import argparse
import csv
import datetime
import logging
import os
import sys


def get_experts(csv_file):
    # experts.csv should have name in 1st column and code in 2nd
    experts = {}
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f, delimiter='\t') 
        next(csv_reader)
        for line in csv_reader:
            experts[line[0]] = line[1]
    return experts

def validate_code(object_id, code_ec, not_ec):
    if not code_ec and not not_ec:
        logging.error("{}: No CODE_EC, not NOT_EC".format(object_id))
    #     return "No CODE_EC, not is NOT_EC"
    # return

def validate_date(object_id, obs_date):
    if not obs_date:
        logging.error("{}: No date!".format(object_id))
    START_DATE = datetime.date(2020, 3, 1)
    END_DATE = datetime.date(2020, 12, 1)
    # ank_date = datetime.datetime.strptime(obs_date, '%d.%m.%y').date()
    if obs_date.date() > END_DATE or obs_date.date() < START_DATE:
       logging.error("{}: bad date! ({})".format(object_id, obs_date.date()))

def validate_polygon_number(object_id, obs_code, number):
    number_parts = number.split("_")
    if len(number_parts) != 2:
        logging.error("{}: no underscore in polygon number".format(object_id))
        return
    if number_parts[0] != obs_code:
        logging.error("{}: polygon number must start with observer code".format(object_id))
        return
    if not number_parts[1].isdigit():
        logging.error("{}: polygon number must end with number".format(object_id))

def validate_form_number(object_id, obs_code, number, not_ec):
    if not_ec:
        if number:
            logging.error("{}: not_ec polygons must not have form number".format(object_id))
        return
    number_parts = number.split("_")
    if len(number_parts) != 3:
        logging.error("{}: no 2 underscores in form number".format(object_id))
        return
    if number_parts[0] != obs_code:
        logging.error("{}: form number must start with observer code".format(object_id))
        return
    if not number_parts[1].isdigit() or not number_parts[2].isdigit():
        logging.error("{}: form number must end with 2 numbers".format(object_id))

def validate_percent(object_id, perc_euh1, perc_euh2, perc_euh3, perc_not_euh):
    if not perc_euh1 and not perc_not_euh:
        logging.error("{}: no percent".format(object_id))
        return
    total_perc = (perc_euh1 or 0) + (perc_euh2 or 0) + \
        (perc_euh3 or 0) + (perc_not_euh or 0)
    if total_perc != 100:
        logging.error("{}: incorrect percent".format(object_id))

def run_validation(fc, fields,experts): # fc -- sortcut for Feature Class
    logging.info("Validating {}".format(fc))
    with arcpy.da.SearchCursor(fc, fields) as cursor:
        for row in cursor:
            object_id = row[10]
            code_ec = row[0]
            not_ec = row[1]
            obs_date = row[2]
            observer =  row[3].encode("utf-8")
            obs_code = experts.get(observer)
            polygon_number = row[4]
            form_number = row[5]
            perc_euh1 =  row[6]
            perc_euh2=  row[7]
            perc_euh3=  row[8]
            perc_not_euh=  row[9]
            validate_code(object_id, code_ec, not_ec)
            validate_date(object_id, obs_date)
            validate_polygon_number(object_id, obs_code, polygon_number)
            validate_form_number(object_id, obs_code, form_number, not_ec)
            validate_percent(object_id, perc_euh1, perc_euh2, perc_euh3, perc_not_euh)

def main():
    WORKDIR = os.getcwd()
    logging.basicConfig(
        filename="{}/validate.log".format(WORKDIR),
        format="%(asctime)s : %(levelname)s : %(message)s",
        level=logging.INFO,
    )
    logging.info("Validation started")
    experts_file = os.path.join(WORKDIR, 'experts.csv')
    experts = get_experts(experts_file)
    fields =  [
        "CODE_EC",
        "NOT_EC",
        "OBS_DATE",
        "OBSERVER",
        "POLYGON_NUMBER",
        "FORM_NUMBER",
        "PERCENTAGE_EC",
        "PERCENTAGE_EC2",
        "PERCENTAGE_EC3",
        "PERCENTAGE_NOT_EC",
        "OBJECTID"]
    parser = argparse.ArgumentParser(description='Validate Habitat_poly in .gdb')
    parser.add_argument('gdb', nargs='*', default=None, help='name(s) of .gdb to process')
    args = parser.parse_args()
    gdb_list = []
    if args.gdb:
        for el in args.gdb:
            if el.endswith('.gdb') and os.path.exists(os.path.join(WORKDIR, el)):
                gdb_list.append(el)
            else:
                print "{} is not valid .gdb".format(el)
    else:
        for el in os.listdir(WORKDIR):
            if el.endswith('.gdb'):
                gdb_list.append(el)
    for gdb in gdb_list:
        gdb_path = os.path.join(WORKDIR, gdb)
        if arcpy.Exists(gdb_path + "\Habitat_poly"):
            fc = gdb_path + "\Habitat_poly"
            run_validation(fc, fields, experts)
    logging.info("Validation ended\n")
    

if __name__ == "__main__":
    main()
