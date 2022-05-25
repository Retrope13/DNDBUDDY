import PC
import Weapon
import Armor
import dearpygui.dearpygui as dpg
from Reader import readWeaponFile, readArmorFile

weaponList = []
armorList = readArmorFile()

stats = []
inventory = []
p1 = PC.PC()

def weaponPurchase(): ##Allows user to click buy after selecting desired weapons
    try:
        dpg.delete_item("Inv")
    except:
        pass
    bill = 0
    itemized = []
    global weaponList
    for i in range(32):
        if dpg.get_value(str(i)):
            nameLen = len(weaponList[i].name)
            itemized.append(weaponList[i].name + ' '*(15-nameLen) + weaponList[i].damage)
            bill += int(weaponList[i].Price)
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
    for i in range(13):
        if dpg.get_value(str(i)):
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
    print(p1.stats)


def firstStep(): ##creates dpg context, viewport, and window
    global weaponList
    dpg.create_context()
    dpg.create_viewport(title="DNDBuddy", width = 1000, height=600)
    charWindow()
    weaponList = readWeaponFile() ##array of weapon objects
    weaponShop()  
    lastStep()

def lastStep():
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.show_style_editor()
    dpg.start_dearpygui()
    dpg.destroy_context()

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

def armorShop():##The armors that PCs can buy or sell
    global armorList
    try:
        dpg.delete_item("Wshop")
        dpg.delete_item("Ashop")
        ##dpg.delete_item("Tshop")
    except:
        pass
    with dpg.window(label="Shop", width=200, height=560, pos=[600, 0], no_title_bar=True, tag="Ashop"):
        with dpg.tab_bar(tag="tabbar"):
            dpg.add_tab_button(label="Weapons", callback=weaponShop)
            dpg.add_tab_button(label="Armor") ##Add callback to destroy Wshop or Tshop and construct armor shop (maybe try catch?)
            dpg.add_tab_button(label="Trinkets")
        for i in range(len(armorList)):
            nameLen = len(armorList[i].name)
            dpg.add_checkbox(label=armorList[i].name + ' '*(15-nameLen) + armorList[i].Price, tag=str(i))
        dpg.add_button(label="Buy", callback=armorPurchase)
        dpg.add_button(label="Sell", callback=armorSell, pos=[50, 330])

def weaponShop(): ##The weapons that PCs can buy or sell
    global weaponList
    try:
        dpg.delete_item("Ashop")
        dpg.delete_item("Wshop")
        ##dpg.delete_item("Tshop")
    except:
        pass
    with dpg.window(label="Shop", width=200, height=560, pos=[600, 0], no_title_bar=True, tag="Wshop"):
        with dpg.tab_bar(tag="tabbar"):
            dpg.add_tab_button(label="Weapons")
            dpg.add_tab_button(label="Armor", callback=armorShop) ##Add callback to destroy Wshop or Tshop and construct armor shop (maybe try catch?)
            dpg.add_tab_button(label="Trinkets")
        for i in range(len(weaponList)):
            nameLen = len(weaponList[i].name)
            dpg.add_checkbox(label=weaponList[i].name + ' '*(15-nameLen) + weaponList[i].Price, tag=str(i))
        dpg.add_button(label="Buy", callback=weaponPurchase)
        dpg.add_button(label="Sell", callback=weaponSell, pos=[50, 745]) ##Line up with buy button

def charInv(): ##eventually this should be a series of checkboxes so the user can equip items
    with dpg.window(label="Inventory", width = 200, height = 560, pos=[800, 0], no_title_bar=True, tag="Inv"):
        for i in p1.inventory:
            dpg.add_checkbox(label = i)

if __name__ == "__main__":
    firstStep()


##To find modifier it's (str-10) / 2