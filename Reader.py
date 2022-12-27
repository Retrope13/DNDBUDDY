import classes.Weapon as Weapon
import classes.Armor as Armor
import classes.Spell as Spell

weaponList = []
armorList = []
spellList = []

Weapons = []
Armors = []
Spells = []

def readWeaponFile():
    global weaponList
    weaponFile = open('ItemFiles/Weapons.txt', 'r')
    holder = []
    for line in weaponFile:
        holder = line.split()
        w1 = Weapon.Weapon(holder.pop(), holder.pop(), holder.pop(), holder.pop())
        weaponList.append(w1)
    return weaponList

def readArmorFile():
    global armorList
    armorFile = open("ItemFiles/armor.txt")
    holder = []
    for line in armorFile:
        holder = line.split()
        ar1 = Armor.Armor(holder.pop(), holder.pop(), holder.pop())
        armorList.append(ar1)
    return armorList

def readSpellFile():
    global spellList
    spellFile = open('ItemFiles/Spells.txt', 'r')
    holder = []
    for line in spellFile:
        holder.append(str(line.strip()))
        s1 = Spell.Spell(str(holder.pop()))
        spellList.append(s1)
    return spellList

def getStats(player, holder):
    tempStat = ""
    stats = []
    for i in holder:
        if i != " ":
            tempStat += i
        else:
            stats.append(int(tempStat))
            tempStat = ""
    stats.append(int(tempStat))
    player.stats = stats

def getInv(charFile):
    holder = []
    inventory = []
    word = ""
    while True:
        char = charFile.read(1)
        if char == ']':
            break
        elif char == '[' or char == '\n' or char == '\'':
            pass
        elif char == ' ':
            if word != '':
                holder.append(word)
            word = ''
        else:
            word += char
    holder.append(word)
    for i in range(len(holder)):
        if i == 0 or i % 2 == 0:
            inventory.append(holder.pop(0))
        else:
            holder.pop(0)
    return inventory

def readSpells(charFile):
    holder = []
    line = ""
    while True:
        char = charFile.read(1)
        if char == ']':
            break
        elif char == "\"" or char == "\n" or char == "[":
            pass
        elif char == ",":
            holder.append(line)
            line = ""
        else:
            line += char
    holder.append(line)
    return holder        

def readCharFile(fileName, player):
    global Armors, Weapons, Spells
    charFile = open(str(fileName), 'r')
    player.name = charFile.readline()
    player.char_class = charFile.readline()
    player.gold = int(charFile.readline())
    player.level = int(charFile.readline())
    holder = []
    while True:
        char = charFile.read(1)
        if char == ']' or char == '\n':
            break
        elif char == '[' or char == ',' or char == ']' or char == '\n':
            pass
        else:
            holder.append(char)

    getStats(player, holder)
    Weapons = getInv(charFile)
    Armors = getInv(charFile)
    Spells = readSpells(charFile)
    return Weapons

def getArmors():
    return Armors

def getSpells():
    return Spells

if __name__ == "__main__":
    readWeaponFile()
    readArmorFile()
    readSpellFile()