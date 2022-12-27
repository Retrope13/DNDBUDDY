import classes.PC as PC
import dearpygui.dearpygui as dpg
from Reader import readCharFile, readSpellFile, readWeaponFile, readArmorFile, getArmors, getSpells
from charWindow import loadImage, imagePopup
import popups
import os

viewport = 0

weaponList = []
armorList = []
spellList = []

tabListShop = ["Wshop", "Ashop", "Sshop"]
tabOpenShop = [0]*3

stats = []
Weapons = []
Armors = []
Spells = []
choice = 0
p1 = PC.PC()

def close():
    try:
        dpg.delete_item("pop")
    except:
        pass

def createFile():
    fileName = dpg.get_value("filename")
    try:
        os.remove(fileName)
    except:
        pass
    exportFile = open(fileName, "a")
    exportFile.write(p1.printChar())
    close()

def setValues():
    dpg.set_value("name", p1.name)
    dpg.set_value("level", p1.level)
    dpg.set_value("class", p1.char_class)
    dpg.set_value("gold", p1.gold)
    dpg.set_value("str", p1.stats[0])
    dpg.set_value("dex", p1.stats[2])
    dpg.set_value("wis", p1.stats[4])
    dpg.set_value("con", p1.stats[1])
    dpg.set_value("int", p1.stats[3])
    dpg.set_value("char", p1.stats[-1])

def weaponSelect(charFile):
    global Weapons, weaponList
    Weapons = readCharFile(charFile, p1)
    p1.Weapons = []
    weaponNames = []
    ##weaponShop()
    for i in range(len(weaponList)):
        weaponNames.append(weaponList[i].name)

    for i in range(len(Weapons)):
        try:
            weaponNames.index(Weapons[i])
        except:
            if Weapons[i] != '':
                print("Weapon: " + Weapons[i] + " was not found in armor file, removing...")
                Weapons[i] = ''
    try:
        while True:
            Weapons.remove('')
    except:
        pass

    for i in range(len(weaponList)):
        if weaponList[i].name == Weapons[0]:
            dpg.set_value(str(weaponList[i]), True)
            Weapons.pop(0)
        if len(Weapons) == 0:
            break
    weaponPurchase(True)

def armorSelect():
    global Armors, armorList
    Armors = getArmors()
    p1.armors = []
    dpg.delete_item("Wshop")
    armorShop()
    armorNames = []
    for i in range(len(armorList)):
        armorNames.append(armorList[i].name)

    for i in range(len(Armors)):
        try:
            armorNames.index(Armors[i])
        except:
            if Armors[i] != '':
                print("Armor: " + Armors[i] + " was not found in armor file, removing...")
                Armors[i] = ''
                
    try:
        while True:
            Armors.remove('')
    except:
        pass
    if len(Armors) > 0:
        for i in range(len(armorList)):
            if armorList[i].name == Armors[0]:
                dpg.set_value(armorList[i].name, True)
                Armors.pop(0)
            if len(Armors) == 0:
                break
        armorPurchase(True)

def spellSelect():
    global Spells
    Spells = getSpells()
    spellNames = []
    dpg.delete_item("Ashop")
    spellShop()
    print(Spells)
    for i in range(len(spellList)):
        spellNames.append(spellList[i].name)

    for i in range(len(Spells)):
        try:
            spellNames.index(Spells[i].strip())
        except:
            if Spells[i] != '':
                print("Spell:" + Spells[i] + " was not found in spell file, removing...")
                Spells[i] = ''
    
    try:
        while True:
            Spells.remove('')
    except:
        pass

    for i in range(len(spellList)):
        if spellList[i].name == Spells[0].strip():
            dpg.set_value(spellList[i].name, True)
            Spells.pop(0)
        if len(Spells) == 0:
            break
    learnSpells()

def getCharFile():
    global weaponList, Armors, Weapons, Spells
    charFile = dpg.get_value("filename")
    weaponSelect(charFile)
    armorSelect()
    spellSelect()
    setValues()
    close()


def importChar():
    with dpg.window(label="Importing Character", tag="pop", modal=True, on_close=close):
        dpg.add_input_text(label="filename", tag="filename")
        dpg.add_button(label="confirm", callback=getCharFile)
        dpg.add_button(label="cancel", callback=close)
    

def exportChar():
    with dpg.window(label="Saving Character", tag="pop", modal=True, on_close=close):
        dpg.add_input_text(label="filename", tag="filename" )
        dpg.add_button(label="confirm", callback=createFile)
        dpg.add_button(label="cancel", callback=close)

def selection(sender):
    if sender == '0':
        close()
        popups.weaponPopup()
    elif sender == '1':
        close()
        popups.armorPopup()
    else:
        close()
        popups.spellPopup()

def homebrewPopup():
    with dpg.window(label="Which type of item would you like to make?", tag="pop", modal=True, on_close=close):
        dpg.add_button(label="Weapon", tag="0", callback=selection)
        dpg.add_button(label="Armor", tag="1", callback=selection)
        dpg.add_button(label="Spell", tag="2", callback=selection)

def saveChar(): ##Saves the character properties for later use
    global stats
    stats.clear()
    p1.name = dpg.get_value("name")
    p1.level = dpg.get_value("level")
    p1.char_class = dpg.get_value("class")
    p1.gold = dpg.get_value("gold")

    stats.append(dpg.get_value("str"))
    stats.append(dpg.get_value("con"))
    stats.append(dpg.get_value("dex"))
    stats.append(dpg.get_value("int"))
    stats.append(dpg.get_value("wis"))
    stats.append(dpg.get_value("char"))
    p1.stats = stats
    exportChar()

def weaponPurchase(imported = False): ##Allows user to click buy after selecting desired weapons
    try:
        dpg.delete_item("Inv")
    except:
        pass
    bill = 0
    itemized = []
    global weaponList, Weapons
    for i in range(len(weaponList)):
        if dpg.get_value(str(weaponList[i])):
            nameLen = len(weaponList[i].name)
            itemized.append(weaponList[i].name + ' '*(15-nameLen) + weaponList[i].damage)
            bill += int(weaponList[i].Price)
            Weapons.append(weaponList[i])
            if imported == True:
                bill = 0
    if bill <= p1.gold:
        p1.weapons += itemized
        p1.gold -= bill
        p1.weapons.sort()
        dpg.set_value("gold", value=p1.gold)
        dpg.delete_item("Wshop")
        weaponShop()
        charWeaponInv()
    else:
        print("CAN'T BUY")

def armorPurchase(imported = False):
    try:
        dpg.delete_item("Inv")
    except:
        pass
    bill = 0
    itemized = []
    global armorList, Armors
    for i in range(len(armorList)):
        if dpg.get_value(armorList[i].name):
            nameLen = len(armorList[i].name)
            itemized.append(armorList[i].name + ' '*(16-nameLen) + armorList[i].ac)
            Armors.append(armorList[i])
            bill += int(armorList[i].Price)
            if imported == True:
                bill = 0
    if bill <= p1.gold:
        p1.armors += itemized
        p1.gold -= bill
        p1.armors.sort()
        dpg.set_value("gold", value=p1.gold)
        dpg.delete_item("Ashop")
        armorShop()
        charArmorInv()
    else:
        print("CAN'T BUY")

def learnSpells():
    try:
        dpg.delete_item("Inv")
    except:
        pass
    itemized = []
    global spellList, Spells
    for i in range(len(spellList)):
        if dpg.get_value(spellList[i].name):
            itemized.append(str(spellList[i].name)) ##It's having a hard time with Purge of Gyrax, Rotting Curse of Ufrestra, and Rightouness of Heroine it's a reading issue
            Spells.append(str(spellList[i].name))
    p1.spells += itemized
    p1.spells.sort()
    dpg.delete_item("Sshop")
    spellShop()
    charSpellInv()

def addHomebrew():
    homebrewPopup()

def unlearnSpell():
    global spellList, Spells
    for i in range(len(spellList)):
        if dpg.get_value(str(spellList[i].name)):
            try:
                pos = p1.spells.index(spellList[i].name)
            except:
                pos = -1
            if pos != -1:
                p1.spells.pop(pos)
                Spells.remove(spellList[i])
                dpg.delete_item("Inv")
                dpg.delete_item("Sshop")
                spellShop()
                charSpellInv()
            else:
                print("Can't unlearn a spell you don't know")

def weaponSell(): ##Can only sell one item at a time for now
    global weaponList, Weapons
    for i in range(len(weaponList)): 
        if dpg.get_value(str(weaponList[i])):
            try:
                pos = p1.weapons.index(weaponList[i].name + ' '*(15-len(weaponList[i].name)) + weaponList[i].damage)
            except:
                pos = -1
            if pos != -1:
                p1.weapons.pop(pos)
                Weapons.remove(weaponList[i])
                p1.gold += int(weaponList[i].Price)
                dpg.set_value("gold", value=p1.gold)
                dpg.delete_item("Inv")
                dpg.delete_item("Wshop")
                weaponShop()
                charWeaponInv()
            else:
                print("Can't sell weapon you don't own")

def armorSell():
    global armorList, Armors
    for i in range(len(armorList)):
        if dpg.get_value(armorList[i].name):
            try:
                pos = p1.armors.index(armorList[i].name + ' '*(16-len(armorList[i].name)) + armorList[i].ac)
            except:
                pos = -1
            if pos != -1:
                p1.armors.pop(pos)
                Armors.remove(armorList[i])
                p1.gold += int(armorList[i].Price)
                dpg.set_value("gold", value=p1.gold)
                dpg.delete_item("Inv")
                dpg.delete_item("Ashop")
                armorShop()
                charArmorInv()
            else:
                print("Can't sell armor you don't own")


def charWindow():
    with dpg.window(label="Character", width=400, height=300, no_title_bar=True):
        dpg.add_input_text(label="Name", tag = "name")
        dpg.add_input_text(label="Class", tag = "class")
        dpg.add_input_int(label="Gold", tag="gold")
        dpg.add_input_int(label = "level", default_value = p1.level, tag="level")
        dpg.add_slider_int(label="HP", max_value= 100) ##Change max_val to increase or decrease health

        dpg.add_input_int(label="Strength", tag="str", width=75)
        dpg.add_input_int(label="Constitution", tag="con", width=75, pos=[193, 123])
        dpg.add_input_int(label="Dexterity", tag="dex", width=75)
        dpg.add_input_int(label="Intelligence", tag="int", width=75, pos=[193, 146])
        dpg.add_input_int(label="Wisdom", tag="wis", width=75)
        dpg.add_input_int(label="Charisma", tag="char", width=75, pos=[193, 169])
        dpg.add_button(label="Add Item", callback=addHomebrew)
        dpg.add_button(label="Save Character", callback=saveChar)
        dpg.add_button(label="Import", callback=importChar)
        dpg.add_button(label="Character Image", callback=imagePopup)

def armorShop():##The armors that PCs can buy or sell
    global armorList, tabOpenShop, tabListShop
    tabOpenShop[0] = dpg.does_item_exist("Wshop")
    tabOpenShop[2] = dpg.does_item_exist("Sshop")
    if tabOpenShop[0] == True:
        dpg.delete_item("Wshop")
    if tabOpenShop[2] == True:
        dpg.delete_item("Sshop")
    with dpg.window(label="Shop", width=200, height=560, pos=[600, 0], no_title_bar=True, tag="Ashop"):
        with dpg.tab_bar(tag="tabbar"):
            dpg.add_tab_button(label="Weapons", callback=weaponShop)
            dpg.add_tab_button(label="Armor")
            dpg.add_tab_button(label="Trinkets")
            dpg.add_tab_button(label= "Spells", callback=spellShop)
        for i in range(len(armorList)):
            nameLen = len(armorList[i].name)
            dpg.add_checkbox(label=armorList[i].name + ' '*(15-nameLen) + armorList[i].Price, tag=armorList[i].name)
        dpg.add_button(label="Buy", callback=armorPurchase)
        dpg.add_button(label="Sell", callback=armorSell)

def spellShop():
    global spellList, tabOpenShop, tabListShop
    tabOpenShop[0] = dpg.does_item_exist("Wshop")
    tabOpenShop[1] = dpg.does_item_exist("Ashop")
    if tabOpenShop[0] == True:
        dpg.delete_item("Wshop")
    if tabOpenShop[1] == True:
        dpg.delete_item("Ashop")
    with dpg.window(label = "Shop", autosize=True, no_title_bar=True, tag="Sshop", pos=[600, 0]):
        with dpg.tab_bar(tag="tabbar"):
            dpg.add_tab_button(label="Weapons", callback=weaponShop)
            dpg.add_tab_button(label="Armor", callback=armorShop)
            dpg.add_tab_button(label="Trinkets")
            dpg.add_tab_button(label="Spells")
        for i in range(len(spellList)):
            dpg.add_checkbox(label=spellList[i].name, tag=spellList[i].name)
        dpg.add_button(label = "Add Spell", callback=learnSpells)
        dpg.add_button(label = "Remove Spell", callback=unlearnSpell)

def weaponShop(): ##The weapons that PCs can buy or sell
    global weaponList, tabOpenShop, tabListShop
    tabOpenShop[1] = dpg.does_item_exist("Ashop")
    tabOpenShop[2] = dpg.does_item_exist("Sshop")
    if tabOpenShop[1] == True:
        dpg.delete_item("Ashop")
    if tabOpenShop[2] == True:
        dpg.delete_item("Sshop")
    with dpg.window(label="Shop", width=200, height=560, pos=[600, 0], no_title_bar=True, tag="Wshop"):
        with dpg.tab_bar(tag="tabbar"):
            dpg.add_tab_button(label="Weapons")
            dpg.add_tab_button(label="Armor", callback=armorShop)
            dpg.add_tab_button(label="Trinkets")
            dpg.add_tab_button(label="Spells", callback=spellShop)
        for i in range(len(weaponList)):
            nameLen = len(weaponList[i].name)
            dpg.add_checkbox(label=weaponList[i].name + ' '*(15-nameLen) + weaponList[i].Price, tag=str(weaponList[i]))
        dpg.add_button(label="Buy", callback=weaponPurchase)
        dpg.add_button(label="Sell", callback=weaponSell)

def inventoryType(type):
    global Weapons, Armors, Spells, p1
    if type == "weapon":
        for i in range(len(Weapons)):
            dpg.add_checkbox(label = str(p1.weapons[i]))
    elif type == "armor":
        for i in range(len(Armors)):
            dpg.add_checkbox(label = p1.armors[i])
    elif type == "spell":
        for i in range(len(Spells)):
            dpg.add_checkbox(label = p1.spells[i])

def charArmorInv():
    try:
        dpg.delete_item("Inv")
    except:
        pass
    with dpg.window(label="Weapons", width = 200, height = 560, pos=[800, 0], no_title_bar=True, tag="Inv"):
        with dpg.tab_bar(tag="invBar"):
            dpg.add_tab_button(label="Weapons", callback=charWeaponInv)
            dpg.add_tab_button(label="Armor")
            dpg.add_tab_button(label="Spells", callback=charSpellInv)
        inventoryType("armor")

def charWeaponInv():
    try:
        dpg.delete_item("Inv")
    except:
        pass
    with dpg.window(label="Weapons", width = 200, height = 560, pos=[800, 0], no_title_bar=True, tag="Inv"):
        with dpg.tab_bar(tag="invBar"):
            dpg.add_tab_button(label="Weapons")
            dpg.add_tab_button(label="Armor", callback=charArmorInv)
            dpg.add_tab_button(label="Spells", callback=charSpellInv)
        inventoryType("weapon")

def charSpellInv():
    try:
        dpg.delete_item("Inv")
    except:
        pass
    with dpg.window(label="Spells", width = 200, height = 560, pos=[800, 0], no_title_bar=True, tag="Inv"):
        with dpg.tab_bar(tag="invBar"):
            dpg.add_tab_button(label="Weapons", callback=charWeaponInv)
            dpg.add_tab_button(label="Armor", callback=charArmorInv)
            dpg.add_tab_button(label="Spells")
        inventoryType("spell")

def firstStep(): ##creates dpg context, viewport, and window
    global weaponList, armorList, spellList, viewport
    weaponList = readWeaponFile()
    armorList = readArmorFile()
    spellList = readSpellFile()

    weaponList.sort(key=lambda x: x.name)
    armorList.sort(key=lambda x: x.name)
    spellList.sort(key=lambda x: x.name)

    dpg.create_context()
    dpg.create_viewport(title="DNDBuddy", width = 1000, height=600)
    charWindow()
    weaponShop()
    lastStep()

def lastStep():
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.show_style_editor()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    firstStep()


##To find modifier it's (str-10) / 2