import sys

import colorama

from collection.cafe_collection import CafeCollection
from models.cafe import Cafe
from scraper.cafe_scraper import CafeScraper


class CLI:
    def __init__(self):
        # initializare colorama ca sa functioneze culorile pe windows si linux
        colorama.init(autoreset=True)
        self.collection = CafeCollection()
        self.scraper = CafeScraper()

    def run(self):
        # incarcam datele salvate anterior inainte sa afisam meniul
        self.collection.load()
        print(colorama.Fore.CYAN + "BrewSpot")

        while True:
            self.show_menu()
            optiune = input("Choose an option: ").strip()

            if optiune == "1":
                self.show_cafes()
            elif optiune == "2":
                self.add_cafe()
            elif optiune == "3":
                self.search_cafe()
            elif optiune == "4":
                self.scrape_cafes()
            elif optiune == "5":
                self.save_cafes()
            elif optiune == "0":
                # salvam automat inainte sa iesim ca sa nu pierdem nimic
                self.save_cafes()
                print("Goodbye!")
                break
            else:
                print(colorama.Fore.RED + "Invalid option.")

    def show_menu(self):
        # meniul principal, simplu si la obiect
        print()
        print("1. Show cafes")
        print("2. Add cafe")
        print("3. Search cafe")
        print("4. Scrape cafes from ialoc")
        print("5. Save")
        print("0. Exit")

    def show_cafes(self):
        cafes = self.collection.list_cafes()

        if len(cafes) == 0:
            print("No cafes in the collection.")
            return

        # sortam dupa rating ca sa apara cele mai bune primele
        self.collection.sort_by_rating()

        for i, cafe in enumerate(self.collection.list_cafes(), start=1):
            print(f"{i}. {self.format_cafe(cafe)}")

    def add_cafe(self):
        # singurul camp obligatoriu e numele, restul au valori default
        nume = input("Name: ").strip()

        if nume == "":
            print(colorama.Fore.RED + "Name is required.")
            return

        adresa = input("Address: ").strip()
        pret = input("Price: ").strip()
        program = input("Schedule: ").strip()
        beneficii_text = input("Benefits (comma separated): ").strip()
        rating = self.read_float("Rating (0-5): ")

        # daca userul nu introduce ceva, punem valori de fallback
        if adresa == "":
            adresa = "Unknown address"
        if pret == "":
            pret = "Unknown"
        if program == "":
            program = "Unknown"

        # transformam sirul de beneficii intr-o lista curata
        beneficii = []
        if beneficii_text != "":
            for beneficiu in beneficii_text.split(","):
                beneficii.append(beneficiu.strip())

        cafe = Cafe(nume, adresa, pret, program, beneficii, rating)

        if self.collection.add_cafe(cafe):
            print(colorama.Fore.GREEN + "Cafe added.")
        else:
            print(colorama.Fore.YELLOW + "Cafe already exists.")

    def search_cafe(self):
        # cautarea e case-insensitive si cauta si partial in nume
        nume = input("Search name: ").strip()
        rezultate = self.collection.search_by_name(nume)

        if len(rezultate) == 0:
            print("No cafes found.")
            return

        for i, cafe in enumerate(rezultate, start=1):
            print(f"{i}. {self.format_cafe(cafe)}")

    def scrape_cafes(self):
        print("Reading cafes from ialoc...")
        cafes = self.scraper.scrape_cafes()
        cate_adaugate = self.collection.add_cafes(cafes)
        cate_existau = len(cafes) - cate_adaugate

        print(colorama.Fore.GREEN + f"Added {cate_adaugate} cafes.")

        # ii spunem userului daca unele existau deja ca sa nu se intrebe de ce numarul e mic
        if cate_existau > 0:
            print(colorama.Fore.YELLOW + f"{cate_existau} were already in the list.")

    def save_cafes(self):
        self.collection.save()
        print(colorama.Fore.GREEN + "Data saved.")

    def read_float(self, mesaj):
        # acceptam si virgula in loc de punct ca sa nu enervam utilizatorul roman
        text = input(mesaj).strip()

        if text == "":
            return 0.0

        try:
            return float(text.replace(",", "."))
        except ValueError:
            print(colorama.Fore.YELLOW + "Invalid rating. Using 0.")
            return 0.0

    def format_cafe(self, cafe):
        # daca nu are beneficii, afisam un mesaj explicit in loc sa lasam gol
        beneficii = "no benefits"

        if len(cafe.benefits) > 0:
            beneficii = ", ".join(cafe.benefits)

        return (
            f"{cafe.name} | rating: {cafe.rating} | price: {cafe.price} | "
            f"address: {cafe.address} | schedule: {cafe.program} | benefits: {beneficii}"
        )


def main():
    try:
        app = CLI()
        app.run()
    except KeyboardInterrupt:
        # ctrl+c e o iesire valida, nu trebuie sa afisam erori urate
        print()
        print("Program stopped.")
        sys.exit(130)