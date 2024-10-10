"""Prepare CSV file"""

import os
import csv
import calendar
from datetime import datetime
from datetime import timedelta

date_format = "%Y-%m-%d"

#ORIGIN_CSV_FILE_NAME = 'Renpho_data_short.csv'
#ORIGIN_CSV_FILE_NAME = "Renpho_data.csv"
ORIGIN_CSV_FILE_NAME = "Renpho_data_OTTOBRE2024.csv"
CSV_FILE_NAME_PREPARED = 'Renpho_data_prepared.csv'
CSV_FILE_NAME_WEEKLY = 'Renpho_data_weekly.csv'
CSV_FILE_NAME_MONTHLY = 'Renpho_data_montly.csv'
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
            #print(lines)

        date1[0] = date0[0]

def count_days_off(day0, day1):
    """counts the number of days off"""
    day0_date = day0[0].split()
    day1_date = day1[0].split()

    day0_num = datetime.strptime(day0_date[0], date_format)
    day1_num = datetime.strptime(day1_date[0], date_format)

    return (day1_num - day0_num).days - 1

def calculate_delta(day0, day1, delta_values, days_off):
    """calculate delta arrays"""
    i = 1
    while i < len(day0):
        if day1[i] != '':
            delta_values[i] = float(day1[i]) - float(day0[i])
        i += 1

    i = 1
    while i < len(day0):
        if day1[i] != '':
            delta_values[i] = delta_values[i] / (days_off+1)
        i += 1

def add_miss_date(in_file, out_file):
    """add missed days"""
    print("adding missed days...")

    global TOTAL_DAYS_OFF

    csv_out = csv.writer(out_file, lineterminator='\n')
    csv_in  = csv.reader(in_file)
    headerLine = next(csv_in)
    csv_out.writerow(headerLine)    #writes header

    day0 = next(csv_in)
    delta_values = day0

    for day1 in csv_in:   #day1 = next(csv_in)
        days_off = count_days_off(day0, day1)
        TOTAL_DAYS_OFF += days_off

        if days_off != 0:
            calculate_delta(day0, day1, delta_values, days_off)

        csv_out.writerow(day0)

        #to convert format
        day0[0] = datetime.strptime(day0[0].split()[0], date_format) + timedelta(days=0)

        while days_off:
            #update day0 with data + 1
            day0[0] = day0[0] + timedelta(days=1)

            i = 1
            while i < len(day0):
                if day0[i] != '':
                    day0[i] = str( round(delta_values[i] + float(day0[i]),2 ))
                i += 1

            csv_out.writerow(day0)
            days_off -= 1

        day0 = day1

    csv_out.writerow(day0)

def add_lines(line_in, line_out, no_elements):
    """sum lines"""
    i = 1
    while i < no_elements:
        if line_in[i] != '':
            line_out[i] += float(line_in[i])
        i += 1

def calculate_average(sum_items, no_elements, num_days):
    """calc average"""
    i = 1
    while i < no_elements:
        sum_items[i] = sum_items[i] / num_days
        sum_items[i] = float("{:.2f}".format(sum_items[i]))
        i += 1


def weekly_group():
    """Creates file grouping weeks"""
    with open(CSV_FILE_NAME_PREPARED, mode = 'r', encoding="utf-8") as prep_file, \
        open(CSV_FILE_NAME_WEEKLY, mode = 'w+', encoding="utf-8") as out_file:

        csvFile_out = csv.writer(out_file, lineterminator='\n')
        csvFile_in = csv.reader(prep_file)
        header = next(csvFile_in)
        csvFile_out.writerow(header)
        count_elements = len(header)

        sum_lines = [0.0] * count_elements #creates a list of elements
        week_start = 0

        for lines in csvFile_in:
            # look for next monday:
            if datetime.strptime(lines[0].split()[0], date_format).weekday() == 0:
                #print(lines[0])
                sum_lines = [0] * count_elements
                sum_lines[0] = datetime.strptime(lines[0].split()[0], date_format).date()
                week_start = 1

            add_lines(lines, sum_lines, count_elements)

            # sunday:
            if datetime.strptime(lines[0].split()[0], date_format).weekday() == 6 and week_start:
                calculate_average(sum_lines, count_elements, 7)
                csvFile_out.writerow(sum_lines)


def monthly_group():
    """Creates file grouping months"""
    with open(CSV_FILE_NAME_PREPARED, mode = 'r', encoding="utf-8") as prep_file, \
        open(CSV_FILE_NAME_MONTHLY, mode = 'w+', encoding="utf-8") as out_file:

        csvFile_out = csv.writer(out_file, lineterminator='\n')
        csvFile_in = csv.reader(prep_file)
        header = next(csvFile_in)
        csvFile_out.writerow(header)
        count_elements = len(header)

        sum_lines = [0.0] * count_elements #creates a list of elements
        start = 0
        num_days = 0

        for lines in csvFile_in:
            # look for next monday:
            if datetime.strptime(lines[0].split()[0], date_format).day == 1:
                sum_lines = [0] * count_elements
                sum_lines[0] = datetime.strptime(lines[0].split()[0], date_format).date()
                start = 1
                year = datetime.strptime(lines[0].split()[0], date_format).year
                month = datetime.strptime(lines[0].split()[0], date_format).month
                num_days = calendar.monthrange(year, month)[1]

            add_lines(lines, sum_lines, count_elements)

            # last day of the month:
            if datetime.strptime(lines[0].split()[0], date_format).day == num_days and start:
                calculate_average(sum_lines, count_elements, num_days)
                csvFile_out.writerow(sum_lines)


def trimestral_group():
    """"""

def semestral_group():
    """"""

def manage_file():
    """Remove duplicates and add missed days"""
    with open(CSV_FILE_NAME_PREPARED, mode = 'w', encoding="utf-8") as prep_file, \
        open(ORIGIN_CSV_FILE_NAME, mode = 'r', encoding="utf-8") as origin_file:
        remove_duplicates(origin_file, prep_file)


    with open(CSV_FILE_NAME_PREPARED, mode = 'r', encoding="utf-8") as prep_file, \
        open(CSV_FILE_NAME_TMP, mode = 'w+', encoding="utf-8") as tmp_file:
        add_miss_date(prep_file, tmp_file)

    os.remove(CSV_FILE_NAME_PREPARED)

    try:
        os.rename(CSV_FILE_NAME_TMP, CSV_FILE_NAME_PREPARED)
    except FileExistsError:
        print("Created file " + CSV_FILE_NAME_PREPARED)

    print("Total days off:")
    print(TOTAL_DAYS_OFF)
