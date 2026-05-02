import json
import os

from models.cafe import Cafe


class CafeCollection:
    def __init__(self, filename="dictionar.json"):
        # fisierul json e singurul loc unde stocam datele intre sesiuni
        self.filename = filename
        self.coffeeshops = []

    def add_cafe(self, cafe):
        # acceptam si dict-uri, le convertim la obiect Cafe pe loc
        if isinstance(cafe, dict):
            cafe = Cafe.from_dict(cafe)

        if self.exista_deja(cafe):
            return False

        self.coffeeshops.append(cafe)
        return True

    def add_cafes(self, cafes):
        # returnam cate am adaugat efectiv, util pentru feedback catre user
        cate_adaugate = 0

        for cafe in cafes:
            if self.add_cafe(cafe):
                cate_adaugate += 1

        return cate_adaugate

    def exista_deja(self, cafe):
        # verificam dupa nume si adresa ca sa evitam duplicate din scraping
        for cafe_existenta in self.coffeeshops:
            acelasi_nume = cafe_existenta.name.lower() == cafe.name.lower()
            aceeasi_adresa = cafe_existenta.address.lower() == cafe.address.lower()

            if acelasi_nume and aceeasi_adresa:
                return True

        return False

    def list_cafes(self):
        return self.coffeeshops

    def search_by_name(self, name):
        # cautarea e case-insensitive si functioneaza si cu nume partial
        rezultate = []
        name = name.lower()

        for cafe in self.coffeeshops:
            if name in cafe.name.lower():
                rezultate.append(cafe)

        return rezultate

    def filter_by_rating(self, minimum_rating):
        # utila daca vrei sa afisezi doar localele peste un anumit prag
        rezultate = []

        for cafe in self.coffeeshops:
            if float(cafe.rating) >= minimum_rating:
                rezultate.append(cafe)

        return rezultate

    def sort_by_rating(self):
        # sortare descrescatoare, cel mai bun rating apare primul
        self.coffeeshops.sort(key=lambda cafe: float(cafe.rating), reverse=True)

    def remove_by_name(self, name):
        # stergem toate intrarile cu acel nume si returnam cate am sters
        cate_sterse = 0
        lista_noua = []
        name = name.lower()

        for cafe in self.coffeeshops:
            if cafe.name.lower() == name:
                cate_sterse += 1
            else:
                lista_noua.append(cafe)

        self.coffeeshops = lista_noua
        return cate_sterse

    def save(self):
        # convertim fiecare obiect la dict inainte sa scriem in json
        lista = []

        for cafe in self.coffeeshops:
            lista.append(cafe.dictionar())

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(lista, file, ensure_ascii=False, indent=2)

    def load(self):
        self.coffeeshops = []

        # daca fisierul nu exista inca, nu e o eroare, returnam lista goala
        if not os.path.exists(self.filename):
            return self.coffeeshops

        with open(self.filename, "r", encoding="utf-8") as file:
            try:
                lista = json.load(file)
            except json.JSONDecodeError:
                # fisier corupt sau gol, pornim cu lista curata
                lista = []

        for item in lista:
            self.add_cafe(Cafe.from_dict(item))

        return self.coffeeshops

    def clear(self):
        # folosit mai ales in teste ca sa resetam starea
        self.coffeeshops = []

    def __len__(self):
        return len(self.coffeeshops)