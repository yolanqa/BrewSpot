import json
import csv
import os
from models.cafe import Cafe

#salvam in json
def salveaza(coffeeshops):
    with open("dictionar.json", "w", encoding = "utf-8") as f:
        json.dump([c.dictionar() for c in coffeeshops], f)


#incarcam inapoi din json in aplicatie
def incarca():
    with open("dictionar.json", "r", encoding = "utf-8") as f:
        dictionar = json.load(f)
