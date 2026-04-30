import json
import csv
import os
from models.cafe import Cafea


with open("dictionar.json", "w", encoding = "utf-8") as f:
    json.dump([c.dictionar() for c in coffeeshops], f)




with open("dictionar.json", "r", encoding = "utf-8") as f:
    dictionar = json.load(f)
