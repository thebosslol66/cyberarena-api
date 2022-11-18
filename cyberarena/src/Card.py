class Card :
    def __init__(self, name, cost, healthpoints , attack, defense, description) :
        self.name = name
        self.cost = cost
        self.attack = attack
        self.defense = defense
        self.healthpoints = healthpoints
        self.description = description

    def getHP(self) -> int:
        return self.healthpoints
    def getAttack(self) -> int:
        return self.attack
    def getDefense(self) -> int:
        return self.defense
    def getDescription(self) -> str:
        return self.description
    def getCost(self) -> int:
        return self.cost
    def attackCard(self,card: Card) -> int:
        if self.attack > card.healthpoints():
            return 1
        else:
            return -1
    def ReceiveDamage(self, damage : int) -> None:
        self.defense = self.defense - damage
        if self.defense <= 0:
            self.healthpoints = self.healthpoints + self.defense
            self.defense = 0
    def isAlive(self) -> bool:
        if self.healthpoints > 0:
            return True
        else:
            return False
    def __str__(self) :
        return self.name + " (" + str(self.cost) + ") : " + str(self.attack) + "/" + str(self.defense) + " : " + self.description

