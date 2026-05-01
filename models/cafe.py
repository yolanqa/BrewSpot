class Cafe:
    def __init__(self, name, address, price, program, benefits, rating):
        self.name = name
        self.address = address
        self.price = price
        self.program = program
        self.benefits = benefits
        self.rating = rating

    def __str__(self):
        return f"Cafenea: {self.name}"
    
    def dictionar(self):
        d ={"name":self.name,
            "address": self.address,
            "price": self.price,
            "program": self.program,
            "benefits": self.benefits,
            "rating": self.rating}
        return d
    @staticmethod
    def from_dict(d):
        cafea = Cafe(name = d["name"], 
                     address = d["address"],
                     price = d["price"],
                     program = d["program"],
                     benefits = d["benefits"],
                     rating = d["rating"])
        return cafea
