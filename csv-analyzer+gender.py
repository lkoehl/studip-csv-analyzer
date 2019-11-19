# -*- coding: utf-8 -*-
import csv
import numpy as np
import matplotlib.pyplot as plt
import gender_guesser.detector as gender

DELIMITER = ";"
FILE = "list.csv"



class Student:
    def __init__(self, group, name, surname, id, login, courses):
        self.group = group
        self.name = name
        self.surname = surname
        self.id = id
        self.login = login
        self.courses = courses

    def get_group(self):
        return self.group

    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

    def get_id(self):
        return self.id

    def get_login(self):
        return self.login

    def get_courses(self):
        return self.courses

    def get_areas(self):
        areas = []
        for course in self.courses:
            areas.append(course["area"])

        return areas

    def get_degree(self):
        degrees = []
        for course in self.courses:
            degrees.append(course["degree"])

        return degrees

    def get_semesters(self):
        semesters = []
        for course in self.courses:
            semesters.append(course["semester"])

        return semesters


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
            if(row["Anrede"] == "Herr"):
                studiengaengeM.append(row["Studiengänge"]) 
                studiengaengeAll.append(row["Studiengänge"]) 
            if(row["Anrede"] == "Frau"):
                studiengaengeAll.append(row["Studiengänge"])

            #if(d.get_gender(row["Vorname"]) == "male" or d.get_gender(row["Vorname"]) == "mostly_male"):
            #    studiengaengeM.append(row["Studiengänge"]) 
            #    studiengaengeAll.append(row["Studiengänge"]) 
            #if (d.get_gender(row["Vorname"]) == "female" or d.get_gender(row["Vorname"]) == "mostly_female"):
            #    studiengaengeAll.append(row["Studiengänge"])
                
            
    test = []
    init_studiengaenge(studiengaengeAll)
    init_studiengaenge(studiengaengeM)

    plt.show()


iterate_file()