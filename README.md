# DNDBUDDY
I'm trying to make a more interactive and beginner friendly Dungeons and Dragons companion app to keep track of inventory, spells, and stats.

# Approach
- I intend to use an object oriented design since many items within D&D have their own statistics
- Using vectors to hold my custom classes allows for homebrew items to be added to weapon and armor lists
- Currently the UI is being developed in DearPyGUI because of the simplicity of rendering and the ability to have movable windows

## Goal
- Through a simplistic design that will reminiscient of RPG style inventories I hope to reduce the barrier to entry many first time players face: "Where do I find that?"
- The goal in perpetuity is to implement full body artistic renderings of several races within D&D as well as armor and weapons to help new players suspend their disbelief

### File Breakdown
1. DNDBuddy.py
- The UI where the classes can interact and the user can input their stats, gold, level, or buy and sell items. This will be the main file that is subject to updates

2. Armor.py & armor.txt
- The python file is the class I've constructed to keep track of the individual properties of each armor
- The txt file simply contains the basic armors found in D&D along with their ac and their price

3. Weapon.py & Weapons.txt
- The python file is the class to keep track of properties of weapons. (I may add range and to hit modifier)
- The txt file is a list of base D&D weapons, their damage, damage type, and price (in gold coins)

4. PC.py
- The class to keep track of player character properties. (I have race and class set to strings to facilitate homebrew.)

5. Reader.py
- This file is responsible for opening the weapons.txt, armor.txt, and spells.txt files and creating the appropriate object. (Spells will be implemented shortly)
