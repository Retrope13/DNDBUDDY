import dearpygui.dearpygui as dpg
from DNDBuddy import Armors, Spells, Weapons, charArmorInv, charSpellInv, charWeaponInv, p1
from classes.Weapon import Weapon
from classes.Armor import Armor
from classes.Spell import Spell

def close():
    try:
        dpg.delete_item("popup")
    except:
        pass

def closeInv():
    try:
        dpg.delete_item("Inv")
    except:
        pass

def weaponPopup():
    with dpg.window(label="Making a weapon", tag="popup", modal=False, on_close=close):
        dpg.add_input_text(label="Weapon name", tag="Wname")
        dpg.add_input_text(label="Damage", tag="damage")
        dpg.add_input_text(label="Damage type", tag="type")
        dpg.add_button(label="add", callback=addWHomebrew)
        dpg.add_button(label="close", callback=close)

def armorPopup():
    with dpg.window(label="Making armor", tag="popup", modal=False, on_close=close):
        dpg.add_input_text(label="Armor name", tag="Aname")
        dpg.add_input_text(label="AC", tag="ac")
        dpg.add_button(label="add", callback=addAHomebrew)
        dpg.add_button(label="close", callback=close)

def spellPopup():
    with dpg.window(label="Making a spell", tag="popup", modal=False, on_close=close):
        dpg.add_input_text(label="Spell name", tag="Sname")
        dpg.add_button(label="add", callback=addSHomebrew)
        dpg.add_button(label="close", callback=close)

def addWHomebrew():
    global p1, Weapons
    wp1 = Weapon(name=dpg.get_value("Wname"), damageType=dpg.get_value("type"), damage="damage")
    p1.weapons.append(dpg.get_value("Wname") + ' '*(15-len(dpg.get_value("Wname"))) + dpg.get_value("damage"))
    Weapons.append(wp1)
    close()
    charWeaponInv()

def addAHomebrew():
    global p1, Armors
    arm1 = Armor(name=dpg.get_value("Aname"), ac=dpg.get_value("ac"))
    p1.armors.append(dpg.get_value("Aname")+ ' '*(15-len(dpg.get_value("Aname"))) + dpg.get_value("ac"))
    Armors.append(arm1)
    close()
    charArmorInv()

def addSHomebrew():
    global p1, Spells
    sp1 = Spell(name=dpg.get_value("Sname"))
    p1.spells.append(dpg.get_value("Sname"))
    Spells.append(sp1)
    close()
    charSpellInv()