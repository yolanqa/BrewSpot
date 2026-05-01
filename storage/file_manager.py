import json
import csv
import os
from models.cafe import Cafe

def salveaza(coffeeshops):
    with open("dictionar.json", "w", encoding = "utf-8") as f:
        json.dump([c.dictionar() for c in coffeeshops], f)

##trebuie facut scrper ul si dupa poate modific cofeeshops

def incarca():
    with open("dictionar.json", "r", encoding = "utf-8") as f:
        dictionar = json.load(f)
