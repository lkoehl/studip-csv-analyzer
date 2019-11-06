import csv



studiengaenge = []


with open('list.csv', mode='r')as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if(line_count == 0):
            print(row)
        studiengaenge.append(row["Studiengänge"])
        line_count += 1;


for studiengang in studiengaenge:
    
