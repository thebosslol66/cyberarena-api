class Card :
    def __init__(self, name, cost, attack, defense, description) :
        self.name = name
        self.cost = cost
        self.attack = attack
        self.defense = defense
        self.description = description



    def __str__(self) :
        return self.name + " (" + str(self.cost) + ") : " + str(self.attack) + "/" + str(self.defense) + " : " + self.description

