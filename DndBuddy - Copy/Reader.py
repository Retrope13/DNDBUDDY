from subprocess import call
import Weapon
import Armor

weaponList = []
armorList = []

def readWeaponFile():
    global weaponList
    weaponFile = open('Weapons.txt', 'r')
    holder = []
    for line in weaponFile:
        holder = line.split()
        w1 = Weapon.Weapon(holder.pop(), holder.pop(), holder.pop(), holder.pop())
        weaponList.append(w1)
    return weaponList

def readArmorFile():
    global armorList
    armorFile = open('armor.txt')
    holder = []
    for line in armorFile:
        holder = line.split()
        ar1 = Armor.Armor(holder.pop(), holder.pop(), holder.pop())
        armorList.append(ar1)
    return armorList



if __name__ == "__main__":
    readWeaponFile()
    readArmorFile()