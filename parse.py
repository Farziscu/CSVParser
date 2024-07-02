"""Prepare CSV file"""

import csv
from datetime import datetime
from datetime import timedelta

date_format = "%Y-%m-%d"

#ORIGIN_CSV_FILE_NAME = 'Renpho_data_short.csv'
ORIGIN_CSV_FILE_NAME = "Renpho_data.csv"
CSV_FILE_NAME_PREPARED = 'Renpho_data_prepared.csv'
CSV_FILE_NAME_TMP = 'Renpho_data_tmp.csv'

TOTAL_DAYS_OFF = 0

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
            print(lines)

        date1[0] = date0[0]

def count_days_off(day0, day1):
    """counts the number of days off"""
    day0_date = day0[0].split()
    day1_date = day1[0].split()

    day0_num = datetime.strptime(day0_date[0], date_format)
    day1_num = datetime.strptime(day1_date[0], date_format)

    return (day1_num - day0_num).days - 1

def add_miss_date(in_file, out_file):
    """add missed days"""
    print("adding missed days...")

    global TOTAL_DAYS_OFF

    csv_out = csv.writer(out_file, lineterminator='\n')
    csv_in  = csv.reader(in_file)
    headerLine = next(csv_in)
    csv_out.writerow(headerLine)    #writes header

    day0 = next(csv_in)

    for day1 in csv_in:   #day1 = next(csv_in)
        days_off = count_days_off(day0, day1)
        TOTAL_DAYS_OFF += days_off

        csv_out.writerow(day0)

        #to convert format
        day0[0] = datetime.strptime(day0[0].split()[0], date_format) + timedelta(days=0)

        while days_off:
            #update day0 with data + 1
            day0[0] = day0[0] + timedelta(days=1)
            csv_out.writerow(day0)
            days_off -= 1

        day0 = day1

    csv_out.writerow(day0)


with open(CSV_FILE_NAME_PREPARED, mode = 'w', encoding="utf-8") as prep_file, \
    open(ORIGIN_CSV_FILE_NAME, mode = 'r', encoding="utf-8") as origin_file:
    remove_duplicates(origin_file, prep_file)


with open(CSV_FILE_NAME_PREPARED, mode = 'r', encoding="utf-8") as prep_file, \
    open(CSV_FILE_NAME_TMP, mode = 'w+', encoding="utf-8") as tmp_file:
    add_miss_date(prep_file, tmp_file)
    #rinominare TMP con PREPARED

print("Total days off:")
print(TOTAL_DAYS_OFF)
