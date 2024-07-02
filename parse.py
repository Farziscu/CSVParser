"""Prepare CSV file"""

import csv
from datetime import date
from datetime import datetime
from datetime import timedelta

date_format = "%Y-%m-%d"

ORIGIN_CSV_FILE_NAME = 'Renpho_data_tmp.csv'
#ORIGIN_CSV_FILE_NAME = "Renpho_data.csv"
CSV_FILE_NAME_PREPARED = 'Renpho_data_prepared.csv'
CSV_FILE_NAME_TMP = 'Renpho_data_tmp.csv'

def remove_duplicates(file, out_file):
    """remove duplicates days"""
    print("removing duplicates...")
    writer = csv.writer(out_file, lineterminator='\n')
    csvFile = csv.reader(file)
    date1 = ["2000-01-01"]
    for lines in csvFile:
        date0 = lines[0].split()

        if date0[0] != date1[0]:
            writer.writerow(lines)
            #print(lines[0] + " -- " + date0[0])
            print(lines)

        date1[0] = date0[0]

def are_consecutive_days(day0, day1):
    """comparing days"""
    day0_date = day0[0].split()
    day1_date = day1[0].split()

    day0_num = datetime.strptime(day0_date[0], date_format)
    day1_num = datetime.strptime(day1_date[0], date_format)

    return bool(day0_num == day1_num - timedelta(days=1))

def add_miss_date(in_file, out_file):
    """add missed days"""
    print("adding missed days...")

    csv_out = csv.writer(out_file, lineterminator='\n')
    csv_in  = csv.reader(in_file)
    headerLine = next(csv_in)
    csv_out.writerow(headerLine)    #writes header

    day0 = next(csv_in)

    for day1 in csv_in:  #day1 = next(csv_in)

        if are_consecutive_days(day0, day1): #day1 == day0 + 1:
            csv_out.writerow(day0)
            day0 = day1
        else:
            csv_out.writerow(day0)
            #update day0 with data + 1
            #a = datetime.strptime(day0[0].split()[0], date_format) + timedelta(days=1)
            day0[0] = datetime.strptime(day0[0].split()[0], date_format) + timedelta(days=1)
            csv_out.writerow(day0)
            day0 = day1

    csv_out.writerow(day0)


with open(CSV_FILE_NAME_PREPARED, mode = 'w', encoding="utf-8") as prep_file, \
    open(ORIGIN_CSV_FILE_NAME, mode = 'r', encoding="utf-8") as origin_file:
    remove_duplicates(origin_file, prep_file)


with open(CSV_FILE_NAME_PREPARED, mode = 'r', encoding="utf-8") as prep_file, \
    open(CSV_FILE_NAME_TMP, mode = 'w', encoding="utf-8") as tmp_file:
    add_miss_date(prep_file, tmp_file)
    #rinominare TMP con PREPARED
