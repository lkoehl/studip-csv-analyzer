# -*- coding: utf-8 -*-
import csv
import numpy as np
import matplotlib.pyplot as plt

DELIMITER = ";"
FILE = "list.csv"






def init_studiengaenge(studiengaengeM):
    result = {}
    for studiengang in studiengaengeM:
        splitted_studiengang = studiengang.split(DELIMITER)
        for single_studiengang in splitted_studiengang:
            stripped_studiengang = single_studiengang.split(",")[0].strip()
            if(len(single_studiengang.split(",")) > 1):
                #print(len(single_studiengang.split(",")))
                type_studiengang = single_studiengang.split(",")[1].strip()
                if(type_studiengang == "2-Fächer-Bachelor"):
                    stripped_studiengang = stripped_studiengang + " 2FB"
                if(stripped_studiengang in result):
                    result[stripped_studiengang] = result[stripped_studiengang] + 1
                else:
                    result[stripped_studiengang] = 1

    print(sorted(result.items(), key = lambda kv:(kv[1], kv[0]), reverse=True))
    lists = sorted(result.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    x, y = zip(*lists)
    plt.bar(x, y)
    plt.xticks(rotation=90)
    



def iterate_file():
    studiengaengeM = []
    studiengaengeAll = []
    with open(FILE, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=DELIMITER)
        line_count = 0
        for row in csv_reader:
            if(row["Geschlecht"] == "m"):
                studiengaengeM.append(row["Studiengänge"])
                line_count += 1
            studiengaengeAll.append(row["Studiengänge"])
            line_count += 1
            
    test = []
    init_studiengaenge(studiengaengeAll)
    init_studiengaenge(studiengaengeM)

    plt.show()


iterate_file()
