import re

import requests
from bs4 import BeautifulSoup

from models.cafe import Cafe


class CafeScraper:
    def __init__(self):
        # url-ul listei de cafenele de pe ialoc, filtrat direct pe tip cafenea
        self.url = "https://ialoc.ro/restaurante-bucuresti?tip=cafenea"
        self.headers = {}

    def scrape_cafes(self, url=None):
        if url is None:
            url = self.url

        try:
            pagina = requests.get(url, headers=self.headers, timeout=15)
            pagina.raise_for_status()
        except requests.RequestException as eroare:
            # daca pica internetul sau site-ul nu raspunde, returnam lista goala
            print("Could not read page:", eroare)
            return []

        soup = BeautifulSoup(pagina.text, "html.parser")
        return self.parse_html(soup)

    def parse_html(self, soup):
        cafes = []

        # pe ialoc, fiecare local din lista este intr-un div cu aceste clase
        cards = soup.select(".list-item.venue-link")

        for card in cards:
            nume_tag = card.select_one(".item-name .title")
            adresa_tag = card.select_one(".item-address")
            rating_tag = card.select_one(".rating-numbers")

            # daca nu gasim macar numele, sarim peste card
            if nume_tag is None:
                continue

            nume = self.curata_nume(nume_tag.get_text(strip=True))
            adresa = "Unknown address"
            rating = 0.0

            if adresa_tag is not None:
                adresa = adresa_tag.get_text(" ", strip=True)

            if rating_tag is not None:
                rating = self.citeste_rating(rating_tag.get_text(strip=True))

            # tagurile contin info despre pret si facilitati
            taguri = self.citeste_taguri(card)
            pret = self.citeste_pret(taguri)
            beneficii = self.citeste_beneficii(taguri)

            # programul nu e disponibil in lista, il setam la necunoscut
            cafe = Cafe(nume, adresa, pret, "Unknown", beneficii, rating)
            cafes.append(cafe)

        return self.sterge_duplicate(cafes)

    def curata_nume(self, nume):
        # uneori numele contine un procent de discount sau "Nou pe ialoc", le scoatem
        nume = re.sub(r"\s*-\d+%\s*$", "", nume)
        nume = nume.replace("Nou pe ialoc", "")
        return nume.strip()

    def citeste_rating(self, text):
        # ialoc foloseste virgula ca separator zecimal, trebuie convertit la punct
        text = text.replace(",", ".")
        match = re.search(r"\d+(\.\d+)?", text)

        if match is None:
            return 0.0

        return float(match.group())

    def citeste_taguri(self, card):
        taguri = []

        # preferam atributul title daca exista, altfel luam textul vizibil
        for tag in card.select(".item-tags a"):
            titlu = tag.get("title")
            text = tag.get_text(" ", strip=True)

            if titlu:
                taguri.append(titlu)
            elif text:
                taguri.append(text)

        return taguri

    def citeste_pret(self, taguri):
        # mapam cuvintele cheie de pe site la simboluri de pret mai universale
        text = " ".join(taguri).lower()

        if "accesibil" in text:
            return "$"
        if "moderat" in text:
            return "$$"
        if "premium" in text:
            return "$$$"
        if "exclusivist" in text:
            return "$$$$"

        return "Unknown"

    def citeste_beneficii(self, taguri):
        # cautam cuvinte cheie in taguri ca sa extragem facilitatile importante
        text = " ".join(taguri).lower()
        beneficii = []

        if "wifi" in text or "wi-fi" in text:
            beneficii.append("wifi")
        if "terasa" in text:
            beneficii.append("terasa")
        if "pet friendly" in text:
            beneficii.append("pet friendly")
        if "vegana" in text or "vegan" in text:
            beneficii.append("vegan")

        return beneficii

    def sterge_duplicate(self, cafes):
        # acelasi local poate aparea de mai multe ori pe pagina, il pastram o singura data
        rezultat = []
        nume_vazute = []

        for cafe in cafes:
            if cafe.name.lower() not in nume_vazute:
                rezultat.append(cafe)
                nume_vazute.append(cafe.name.lower())

        return rezultat


if __name__ == "__main__":
    scraper = CafeScraper()
    rezultat = scraper.scrape_cafes()

    for cafe in rezultat:
        print(cafe)
