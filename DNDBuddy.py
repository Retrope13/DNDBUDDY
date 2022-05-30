import classes.PC as PC
import classes.Weapon as Weapon
import classes.Armor as Armor
import dearpygui.dearpygui as dpg
from Reader import readCharFile, readSpellFile, readWeaponFile, readArmorFile

weaponList = readWeaponFile()
armorList = readArmorFile()
spellList = readSpellFile()

tabList = ["Wshop", "Ashop", "Sshop"]
tabOpen = [0]*3

stats = []
inventory = []
p1 = PC.PC()

def close():
    dpg.delete_item("pop")    

def createFile():
    fileName = dpg.get_value("filename")
    exportFile = open(fileName, "a")
    exportFile.truncate(0)
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

def getCharFile():
    global weaponList
    charFile = dpg.get_value("filename")
    inventory = readCharFile(charFile, p1)
    p1.inventory = []
    for i in range(len(weaponList)):
        if weaponList[i].name == inventory[0]:
            dpg.set_value(str(i), True)
            inventory.pop(0)
        if len(inventory) == 0:
            break
    weaponPurchase(True)
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
    global weaponList
    for i in range(len(weaponList)):
        if dpg.get_value(str(i)):
            nameLen = len(weaponList[i].name)
            itemized.append(weaponList[i].name + ' '*(15-nameLen) + weaponList[i].damage)
            bill += int(weaponList[i].Price)
            if imported == True:
                p1.gold += bill
    if bill <= p1.gold:
        p1.inventory += itemized
        p1.gold -= bill
        p1.inventory.sort()
        dpg.set_value("gold", value=p1.gold)
        dpg.delete_item("Wshop")
        weaponShop()
        charInv()
    else:
        print("CAN'T BUY")

def armorPurchase():
    try:
        dpg.delete_item("Inv")
    except:
        pass
    bill = 0
    itemized = []
    global armorList
    for i in range(len(armorList)):
        if dpg.get_value(armorList[i]):
            nameLen = len(armorList[i].name)
            itemized.append(armorList[i].name + ' '*(15-nameLen) + armorList[i].ac)
            bill += int(armorList[i].Price)
    if bill <= p1.gold:
        p1.inventory += itemized
        p1.gold -= bill
        p1.inventory.sort()
        dpg.set_value("gold", value=p1.gold)
        dpg.delete_item("Ashop")
        armorShop()
        charInv()
    else:
        print("CAN'T BUY")

def weaponSell(): ##Can only sell one item at a time for now
    global weaponList
    for i in range(len(weaponList)): 
        if dpg.get_value(str(i)):
            try:
                pos = p1.inventory.index(weaponList[i].name + ' '*(15-len(weaponList[i].name)) + weaponList[i].damage)
            except:
                pos = -1
            if pos != -1:
                p1.inventory.pop(pos)
                p1.gold += int(weaponList[i].Price)
                dpg.set_value("gold", value=p1.gold)
                dpg.delete_item("Inv")
                dpg.delete_item("Wshop")
                weaponShop()
                charInv()
            else:
                print("Can't sell weapon you don't own")

def armorSell():
    global armorList
    for i in range(len(armorList)):
        if dpg.get_value(str(i)):
            try:
                pos = p1.inventory.index(armorList[i].name + ' '*(15-len(armorList[i].name)) + armorList[i].ac)
            except:
                pos = -1
            if pos != -1:
                p1.inventory.pop(pos)
                p1.gold += int(armorList[i].Price)
                dpg.set_value("gold", value=p1.gold)
                dpg.delete_item("Inv")
                dpg.delete_item("Ashop")
                armorShop()
                charInv()
            else:
                print("Can't sell weapon you don't own")


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
        dpg.add_button(label="Save", callback=saveChar)
        dpg.add_button(label="Import", callback=importChar)

def armorShop():##The armors that PCs can buy or sell
    global armorList, tabOpen, tabList
    tabOpen[0] = dpg.does_item_exist("Wshop")
    tabOpen[2] = dpg.does_item_exist("Sshop")
    if tabOpen[0] == True:
        dpg.delete_item("Wshop")
    else:
        dpg.delete_item("Sshop")
    with dpg.window(label="Shop", width=200, height=560, pos=[600, 0], no_title_bar=True, tag="Ashop"):
        with dpg.tab_bar(tag="tabbar"):
            dpg.add_tab_button(label="Weapons", callback=weaponShop)
            dpg.add_tab_button(label="Armor") ##Add callback to destroy Wshop or Tshop and construct armor shop (maybe try catch?)
            dpg.add_tab_button(label="Trinkets")
            dpg.add_tab_button(label= "Spells", callback=spellShop)
        for i in range(len(armorList)):
            nameLen = len(armorList[i].name)
            dpg.add_checkbox(label=armorList[i].name + ' '*(15-nameLen) + armorList[i].Price, tag=str(i))
        dpg.add_button(label="Buy", callback=armorPurchase)
        dpg.add_button(label="Sell", callback=armorSell)

def spellShop():
    global spellList, tabOpen, tabList
    tabOpen[0] = dpg.does_item_exist("Wshop")
    tabOpen[1] = dpg.does_item_exist("Ashop")
    if tabOpen[0] == True:
        dpg.delete_item("Wshop")
    else:
        dpg.delete_item("Ashop")
    with dpg.window(label = "Shop", autosize=True, no_title_bar=True, tag="Sshop", pos=[600, 0]):
        with dpg.tab_bar(tag="tabbar"):
            dpg.add_tab_button(label="Weapons", callback=weaponShop)
            dpg.add_tab_button(label="Armor", callback=armorShop) ##Add callback to destroy Wshop or Tshop and construct armor shop (maybe try catch?)
            dpg.add_tab_button(label="Trinkets")
            dpg.add_tab_button(label="Spells")
        for i in range(len(spellList)):
            dpg.add_checkbox(label=spellList[i].name)
        dpg.add_button(label = "Add Spell")

def weaponShop(): ##The weapons that PCs can buy or sell
    global weaponList, tabOpen, tabList
    tabOpen[1] = dpg.does_item_exist("Ashop")
    tabOpen[2] = dpg.does_item_exist("Sshop")
    if tabOpen[1] == True:
        dpg.delete_item("Ashop")
    elif tabOpen[2] == True:
        dpg.delete_item("Sshop")
    with dpg.window(label="Shop", width=200, height=560, pos=[600, 0], no_title_bar=True, tag="Wshop"):
        with dpg.tab_bar(tag="tabbar"):
            dpg.add_tab_button(label="Weapons")
            dpg.add_tab_button(label="Armor", callback=armorShop) ##Add callback to destroy Wshop or Tshop and construct armor shop (maybe try catch?)
            dpg.add_tab_button(label="Trinkets")
            dpg.add_tab_button(label="Spells", callback=spellShop)
        for i in range(len(weaponList)):
            nameLen = len(weaponList[i].name)
            dpg.add_checkbox(label=weaponList[i].name + ' '*(15-nameLen) + weaponList[i].Price, tag=str(i))
        dpg.add_button(label="Buy", callback=weaponPurchase)
        dpg.add_button(label="Sell", callback=weaponSell)

def charInv(): ##eventually this should be a series of checkboxes so the user can equip items
    with dpg.window(label="Inventory", width = 200, height = 560, pos=[800, 0], no_title_bar=True, tag="Inv"):
        for i in p1.inventory:
            dpg.add_checkbox(label = i)

def firstStep(): ##creates dpg context, viewport, and window
    global weaponList
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