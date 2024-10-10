"""Shows csv file as graph"""

import matplotlib.pyplot as plt
import csv

CSV_FILE_NAME_WEEKLY = 'Renpho_data_weekly.csv'
CSV_FILE_NAME_MONTHLY = 'Renpho_data_montly.csv'

def main_views():
    x = []
    x_label = ''

    y0 = []
    y0_label = ''

    y1 = []
    y1_label = ''

    with open(CSV_FILE_NAME_WEEKLY, mode = 'r', encoding="utf-8") as csv_file:
        plots = csv.reader(csv_file, delimiter = ',')
        header = next(plots)

        x_label = header[0]
        y0_label = header[1]
        y1_label = header[4]

        for row in plots:
            x.append(row[0])
            y0.append(float(row[1]))
            y1.append(float(row[4]))


    fig = plt.figure(figsize=(15, 8))
    axes = fig.add_subplot(111)

    axes2 = axes.twinx()
    axes2.set_ylim(54, 56)

    lns1 = axes.plot(x, y0, color = 'g', linestyle='dashed', marker = '*' , label = y0_label)
    lns2 = axes2.plot(x, y1, color = 'b', linestyle='dashed', marker = 'o', label = y1_label)

    axes.set_xlabel(x_label)
    axes.set_ylabel(y0_label)
    #axes.tick_params(axis='y', labelcolor='g')

    axes2.set_ylabel(y1_label)
    #axes2.tick_params(axis='y', labelcolor='r')

    axes.grid()

    leg = lns1 + lns2
    labs = [l.get_label() for l in leg]
    axes.legend(leg, labs, loc=0)

    plt.title('Weekly weight')
    plt.show()


#----------------------------

# plt.plot(x, y0, color = 'g', linestyle='dashed', marker = '*', label = y0_label)
# plt.plot(x, y1, color = 'b', linestyle='dashed', marker = 'o', label = y1_label)
# 
# plt.xticks(rotation = 25)
# plt.xlabel(x_label)
# plt.ylabel(y0_label)
# plt.ylabel(y1_label)
# plt.title('Weekly weight')
# plt.grid()
# plt.legend()
# plt.show()
