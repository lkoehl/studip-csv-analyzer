# -*- coding: utf-8 -*-
import csv
import numpy as np
import matplotlib.pyplot as plt

DELIMITER = ";"
FILE = "list.csv"



def init_studiengaenge(studiengaenge):
    result = {}
    for studiengang in studiengaenge:
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
    studiengaenge = []
    with open(FILE, mode='r') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=DELIMITER)
        for row in csv_reader:
            studiengaenge.append(row["Studiengänge"])
            
    init_studiengaenge(studiengaenge)

    plt.show()



iterate_file()