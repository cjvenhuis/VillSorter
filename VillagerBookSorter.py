import MClasses as mclass
# ToDo Anvil Cost Calculation included with Cost
# ToDo Villager Statistics showing the ranking for all their books
#     Requires a list of books for each enchantment, sorting by cost
#     and requires a ranking in the villager class

def main():
    # initialize and calculate
    enchantments = initializeEnchantments()
    villagers, enchantments = update(enchantments)

    # begin comparing    
    compare(villagers, enchantments)

def update(enchantments):
    # initialize enchantments and villagers
    enchantments = resetEnchantments(enchantments)
    villagers = getVillagers()
    
    # get best trade results and update enchantments and villagers with new info
    enchantments, villagers = getResults(enchantments, villagers)
    printResults(enchantments, villagers)
    
    return villagers, enchantments

def initializeEnchantments():
    # commented enchantments don't exist in the bedrock version
    # uncomment to use
    data = [("Aqua Affinity",1), ("Bane of Arthropods",5),
            ("Blast Protection",4), #("Curse of Binding",1), ("Curse of Vanishing",1),
            ("Depth Strider",3), ("Efficiency",5), ("Feather Falling",4),
            ("Fire Aspect",2), ("Fire Protection",4), ("Flame",1),
            ("Fortune",3), ("Frost Walker",2), ("Infinity",1), ("Knockback",2), 
            ("Looting",3), ("Luck of the Sea",3), ("Lure",3), ("Mending",1),
            ("Power",5), ("Projectile Protection",4), ("Protection",4),
            ("Punch",2), ("Respiration",3), ("Sharpness",5), ("Silk Touch",1),
            ("Smite",5), #("Sweeping Edge", 3),
            ("Thorns",3), ("Unbreaking",3)]

    # determine minCost - minCost is based on the rank of the enchantment
    enchantments = []
    for ench in data:
        minCost = None
        name = ench[0]
        maxRank = ench[1]
        if maxRank == 1:
            minCost = 5
        elif maxRank == 2:
            minCost = 8
        elif maxRank == 3:
            minCost = 11
        elif maxRank == 4:
            minCost = 14
        elif maxRank == 5:
            minCost = 17
        # special/treasure enchantments minCost is 2x the regular cost
        # might need to add sweeping edge and the curse enchantments to this
        if name == "Mending" or name == "Frost Walker":
            minCost = minCost*2
            
        # create enchantment and add to list
        enchantment = mclass.Enchantment(name, maxRank, minCost)
        enchantments.append(enchantment)
    return enchantments
    
def resetEnchantments(enchantments):
    # should simply reset the statistics without recreating the whole list
    for enchantment in enchantments:
        enchantment.reset()
    return enchantments
    
def compare(villagers, enchantments):
    # fix this function
    # input is annoying and needs to be more versatile. 
    # e.g. being able to exit at any time
    # some parts could be put into a new function, possibly
    inp = input("Add Villager(1) Remove Villager(2) Quit(q/e): ")
    while inp != "e" and inp != "q":
        currentVillagers = []
        for villager in villagers:
            currentVillagers.append(villager.getNumber())

        # Add Villager - putting input stuff here can solve input problems
        if inp == "1":
            try:
                number, newVillager = getVillagerInput(villagers, enchantments)
            except TypeError:
                print("cancelled")
                return
            
            addVillager(number, newVillager)
            villagers, enchantments = update(enchantments)
            
        # Remove Villager
        if inp == "2":
            while True:
                # if input not an int
                try:
                    number = int(input("Which Villager?: "))
                except ValueError:
                    print("invalid input")
                    continue
                
                # if villager DNE
                if number in currentVillagers:
                    break
                else:
                    print("villager doesn't exist")
                    continue
                
            while True:
                # double check - user error sucks
                try:
                    confirm = input("Are you sure?: ").lower()
                except TypeError:
                    print("invalid response")
                    continue
                if confirm == "y" or confirm == "n":
                    break
                
            # everything checks out - commence
            if confirm == "y":
                removeVillager(number)
                villagers, enchantments = update(enchantments)
            elif confirm == "n":
                return

        inp = input("Add Villager(1) Remove Villager(2) Quit(q/e): ")    
    
def getResults(enchantments, villagers):
    # calculate the best costing trade for each enchantment
    for villager in villagers:
        books = villager.getBooks()
        for book in books:
            for enchantment in enchantments:
                if book.getEnch() == enchantment.getName():
                    enchantment.compareCost(book.getCost(), book.getRank(), villager.getNumber())
        
    # rate each villager based on number of good trades
    # possibly get rid of rating, but still need to tell which trade is their best
    for enchantment in enchantments:
        for villager in villagers:
            books = villager.getBooks()
            for book in books:
                if book.getEnch() == enchantment.getName():
                    if enchantment.matchCost(book.getCost(), book.getRank()) == 1:
                        villager.addGoodTrade(book)
    
    return enchantments, villagers

def printResults(enchantments, villagers):
    spl = "|"   # column split
    na = ""     # empty string
    enchLines = getEnchantmentLines(enchantments, spl, na)
    villLines = getVillagerLines(villagers, spl, na)
    
    # all formatting is done such that the column size is versatile
    # i.e. I don't have to make a dozen edits here if anything is changed
    # contents of columns is the responsibility of MClasses
    # lines are created in getEnchantmentLines and getVillagerLines
    
    # make sure there are equal amounts of lines, even if they are dummy lines
    enchLen = len(enchLines)
    villLen = len(villLines)    
    if enchLen < villLen:
        enchDummy = []
        for item in enchLines[0]:
            if item == spl:
                enchDummy.append(spl)
            else:
                enchDummy.append(na)
        while len(enchLines) < len(villLines):
            enchLines.append(enchDummy)    
    elif villLen < enchLen:
        villDummy = []
        for item in villLines[0]:
            if item == spl:
                villDummy.append(spl)
            else:
                villDummy.append(na)                
        while len(villLines) < len(enchLines):
            villLines.append(villDummy)

    # combine lines lists into one list
    i = 0
    lines = []
    while i < len(enchLines):
        div = [spl*3]
        line = enchLines[i] + div + villLines[i]
        lines.append(line)
        i+=1
    
    # calculate size of headers, i.e. the standard for how many columns there are
    length = len(lines[0])
    
    # calculate maximum length of each column
    i = 0
    widths = length*[0]
    while i < length:
        for line in lines:
            if widths[i] < len(str(line[i])):
                widths[i] = len(str(line[i]))                
        i+=1
    
    # print all the lines!
    for line in lines:
        i = 0
        for width in widths:
            # create format size based on column widths and print each element
            widthStr = "{:^" + str(width+1) + "}"
            print(widthStr.format(line[i]), end=na)
            i+=1
            
        # finished
        print(na)

def getVillagerLines(villagers, spl, na):
    lines = []
    # villLines contents are handled here
    # think about getting rid of rating
    
    # header
    line = []
    line.extend(("Number", spl, "Rating", spl, "Good Trades", spl, "Cost"))
    lines.append(line)
    
    # data lines
    for villager in villagers:
        i = 0
        number = villager.getNumber()
        goodTrades = villager.getGoodTrades()
        rating = len(goodTrades)
        
        while i < rating or i == 0:
            # handle first two columns of villager
            line = []
            if i == 0:
                # first row
                line.extend((number, spl, rating, spl))
            else:
                # subsequent rows of the same villager
                line.extend((na, spl, na, spl))

            # handle other columns
            if rating == 0:
                # no good trades, leave empty
                line.extend((na, spl, na))
            else:
                # get a good trade - create strings for columns
                name = goodTrades[i].getEnch()
                rank = goodTrades[i].getRank()
                cost = goodTrades[i].getCost()

                # create enchantment string for column
                enchStr = ""
                
                # rank of trade enchantment in roman numeral form!
                # use this a couple times - make a function?
                rnStr = ""
                if rank == 1:
                    rnStr = "I"
                elif rank == 2:
                    rnStr = "II"
                elif rank == 3:
                    rnStr = "III"
                elif rank == 4:
                    rnStr = "IV"
                elif rank == 5:
                    rnStr = "V"
                enchStr = name + " " + rnStr
                                
                line.extend((enchStr, spl, cost))

            i+=1
            lines.append(line)
            
    return lines

def getEnchantmentLines(enchantments, spl, na):
    lines = []
    # enchLines contents are handled here

    # header
    line = []
    line.extend(("Enchantment", spl, "Cost", spl, "Dif", spl, "Villagers"))
    lines.append(line)
    
    # data lines
    for enchantment in enchantments:
        line = []
        name = enchantment.getName()
        rank = enchantment.getMaxRank()
        cost = enchantment.getCurrentCost()
        
        # diff is the different between the calculated minimum cost and possible
        # minimum cost to show if it can get better
        try:
            diff = cost - enchantment.getMinCost()
        except TypeError:
            diff = "-"
        if diff == 0:
            diff = "="
        
        # create enchantment and villager string for columns
        villagers = enchantment.getVillagers()
        enchStr, villStr = "", ""

        # rank of trade enchantment in roman numeral form!
        # use this a couple times - make a function?
        rnStr = ""
        if rank == 1:
            rnStr = "I"
        elif rank == 2:
            rnStr = "II"
        elif rank == 3:
            rnStr = "III"
        elif rank == 4:
            rnStr = "IV"
        elif rank == 5:
            rnStr = "V"
        enchStr = name + " " + rnStr

        # in case two villagers have the same enchantment for the same cost
        # make a string of numbers separated by commas
        i = 1
        for villager in villagers:
            villStr = villStr + str(villager)
            if len(villagers) > 1 and i != len(villagers):
                villStr = villStr + ", "
            i+=1
            
        line.extend((enchStr, spl, cost, spl, diff, spl, villStr))
        lines.append(line)
        
    return lines
        
def getVillagers():
    villagers = []
    # changes to make:
    # if file DNE, create one - format it?
    # make it so lines don't have numbers in front of them by default
    # still want order to matter, i.e. 1 and 3 can be assigned but 2 is empty

    # open file to get information
    f = open("VillagerBooks.txt", "r")
    if f.mode == "r":
        contents = f.readlines()
        
    # Parse the information into a villager class
    for line in contents:
        line = line.replace("\n", "")
        
        # splits into two, first is the number, second is the list of books
        villager = line.split(":")
        number = int(villager[0])

        # only add a villager if it has books assigned to it
        # i.e. a line without any info is not a villager
        if villager[1] != "":
            books = []
            booklist = villager[1].split(";")
            for book in booklist:
                components = book.split(",")
                ench = components[0]
                rank = int(components[1])
                cost = int(components[2])
                
                b = mclass.Book(ench, rank, cost)
                books.append(b)

            v = mclass.Villager(number, books)
            villagers.append(v)
    
    # done    
    f.close()
    return villagers

def removeVillager(number):
    # open file to get information
    f = open("VillagerBooks.txt", "r")
    if f.mode == "r":
        contents = f.readlines()
    
    # find villager and delete information
    i = len(contents) - 1
    while i >= 0:
        if int(contents[i].split(":")[0]) == number:
            contents.pop(i)
            contents.insert(i, str(number) + ":\n")
        i-=1
    f.close()

    # save changes
    f = open("VillagerBooks.txt", "w")
    f.flush()
    for line in contents:
        f.write(line)    
    f.close()

def addVillager(number, newVillager):    
    # open file to get information
    f = open("VillagerBooks.txt", "r")
    if f.mode == "r":
        contents = f.readlines()
    f.close()
    
    # find the chosen line and add new information to it
    i = len(contents) - 1
    while i >= 0:
        if int(contents[i].split(":")[0]) == number:
            contents.pop(i)
            contents.insert(i, newVillager + "\n")
        i-=1    
            
    # save changes
    f = open("VillagerBooks.txt", "w")
    f.flush()
    for line in contents:
        f.write(line)    
    f.close()
    
def getVillagerInput(villagers, enchantments):
    newVillager = []
    # potentially make it so you can go back a step in this input
    
    # list of villager numbers that exist
    currentVillagers = []
    for villager in villagers:
        currentVillagers.append(villager.getNumber())
        
    while True:
        # check if number is taken
        try:
            number = int(input("Number: "))
        except ValueError:
            print("invalid input")
            continue        

        # pick a number between 1 and... 1,000,000
        if number > 1000000:
            print("number too high")
            continue
        elif number <= 0:
            print("number too low")
            continue
        elif number in currentVillagers:
            print("number taken")
            continue
        else:
            if number > 40:
                # make a list of easter egg outputs and pick on at random?
                # I vote yes
                print("why do you have so many villagers? Wait, don't answer that... carry on...")
            newVillager.extend((number, ":"))
            break
    
    i = 0
    while i < 3:
        i+=1
        # check if it's a valid enchantment
        # this is annoying because it has to be exact - at least change it so
        # capitals don't matter
        # potentially add a feature to guess what enchantment you meant to type
        while True:
            ench = input("Enchantment " + str(i) + ": ")
            valid = False
            enchantment = None
            for e in enchantments:
                if e.getName() == ench:
                    valid = True
                    enchantment = e
                
            if valid == False:
                print("invalid enchantment")
                continue
            else:
                newVillager.extend((enchantment.getName(), ","))
                break
                    
        # check if it's a valid rank
        while True:
            try:
                rank = int(input("Rank: "))
            except ValueError:
                print("invalid input")
                continue
            
            if rank > enchantment.getMaxRank() or rank <= 0:
                print("invalid rank, maximum is", enchantment.getMaxRank())
                continue
            else:
                newVillager.extend((rank, ","))
                break
        
        # check if it's a valid cost
        while True:
            try:
                cost = int(input("Cost: "))
            except ValueError:
                print("invalid input")
                continue
            
            if cost > 64 or cost < 5:
                print("invalid cost")
                continue
            else:
                newVillager.append(cost)
                if(i < 3):
                    newVillager.append(";")
                break

    villagerStr = ""
    for string in newVillager:
        villagerStr+=str(string)

    while True:
        try:
            confirm = input("Add Villager?(Y/N): ").lower()
        except TypeError:
            print("invalid response")
            continue
        if confirm == "y" or confirm == "n":
            break

    if confirm == "y":
        return number, villagerStr
    elif confirm == "n":
        return
        
def villagerRating(villagers, trades):
    # add rank the villagers that appear in trades
    for trade in trades:
        if len(trade) > 2:
            villagers[trade[1]].increaseRating()
            villagers[trade[1]].addGoodTrade(trade)

def testPrint(printing):
    # this makes it easier to remove print statements after debugging but
    # serves no actual use in the program
    print(printing)
             
if __name__ == "__main__":
    main()
    
    
