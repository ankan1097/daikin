import csv

index = 101
with open('CustomerLocationsDay3_3April2017.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        with open('update.sql', 'a') as myfile:
            myfile.write('update customerinfo set latitude = ' + str(row[1]) + ', longitude = ' + str(row[2]) + ' where id = \'' + str(index) + '\';\n')
        index += 1
        if index > 200:
            break
