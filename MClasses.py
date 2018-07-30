class Villager:
    def __init__(self, number, books):
        self.number = number
        self.books = books
        self.goodTrades = []
    
    def getNumber(self):
        return self.number
    
    def getBooks(self):
        return self.books

    def addGoodTrade(self, book):
        self.goodTrades.append(book)
        
    def getGoodTrades(self):
        return self.goodTrades

class Enchantment:
    def __init__(self, name, maxRank, minCost):
        self.name = name
        self.maxRank = maxRank
        self.minCost = minCost
        self.currentCost = None
        self.villagers = []
        
    def reset(self):
        self.currentCost = None
        self.villagers = []
        
    def compareCost(self, cost, rank, villager):
        diff = self.maxRank - rank
        actualCost = cost*(2**diff)
        if self.currentCost == None or actualCost < self.currentCost:
            self.currentCost = actualCost
            self.updateVillager(villager)
        elif actualCost == self.currentCost:
            self.addVillager(villager)
        elif actualCost > self.currentCost:
            return -1
        
    def matchCost(self, cost, rank):
        diff = self.maxRank - rank
        actualCost = cost*(2**diff)
        if actualCost == self.currentCost:
            return 1
        else:
            return 0
        
    def updateCost(self, cost):
        self.currentCost = cost

    def updateVillager(self, villager):
        self.villagers = []
        self.villagers.append(villager)
        
    def addVillager(self, villager):
        self.villagers.append(villager)

    def getName(self):
        return self.name
    
    def getMaxRank(self):
        return self.maxRank
    
    def getMinCost(self):
        return self.minCost
    
    def getCurrentCost(self):
        return self.currentCost
    
    def getVillagers(self):
        return self.villagers

class Book():
    def __init__(self, ench, rank, cost):
        self.ench = ench
        self.rank = rank
        self.cost = cost
        
    def getEnch(self):
        return self.ench

    def getRank(self):
        return self.rank
    
    def getCost(self):
        return self.cost