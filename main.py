import random
import os
import sys
import importlib
import time
import shutil
ORIGINAL_WORKING_DIRECTORY = os.getcwd()

def main(inventory, money, available_fish, difficulty, equipment, save_slot): 
    last_action = "save data"
    print(f"The current save slot is {save_slot[: - 13]}.")
    while True:
        AVAILABLE_ACTIONS = ["help", "fish", "shop", "quit", "view wallet", "view inventory", "save data", "configure saves", "configure difficulty", "edit equipment",]
        action = input('What would you like to do? Type "help" for a list of actions, and as a reminder, you can type "quit" at any time to go back to the previous menu. ').lower()
        if action == "help":
            print(f"Here is a list of available actions")
            print_each_item_in_list(AVAILABLE_ACTIONS)
        elif action == "quit":
            if last_action != "save data":
                confirm_exit_without_save = input('You are about to quit without saving, type "yes" to confirm you want to do this and anything else to go back to save. ')
            if last_action == "save data" or confirm_exit_without_save == "yes":
                print("Sad to see you go! Goodbye!")
                raise SystemExit()
        elif action == "view wallet":
            print(money)
        elif action == "view inventory":
            print_inventory(inventory)
        elif action == "shop":
            money = accessing_shop(inventory, money)
        elif action == "fish":
            fishing(inventory, available_fish, difficulty)
        elif action == "save data":
            save_data_from_session(inventory, money, available_fish, difficulty, equipment, save_slot)
        elif action == "configure saves":
            save_slot_configuration(save_slot)
        elif action == "configure difficulty":
            difficulty = configure_difficulty(difficulty)
        elif action == "edit equipment":
            edit_equipment(equipment, inventory)
        else:
            print("What you entered isn't a valid action, please try again.")
        if action in AVAILABLE_ACTIONS and action != "quit":
            last_action = action

def selling(inventory, money):
    SELL_VALUES = {
        "salmon" : 2,
        "carp" : 1,
        "clownfish" : 3,
        "flounder" : 2,
        "crab" : 3,
        "sardine" : 4
    }
    while True:
        keep_dupes_or_not = input(f'Sell everything or only duplicates? Type "duplicates" to sell only duplicates, and "everything" to sell everything. ').lower()
        if keep_dupes_or_not == "everything":
            for item, amount in list(inventory.items()):
                if item in SELL_VALUES:
                    for count in range(amount):
                        money = money + SELL_VALUES.get(item)
                    del inventory[item]
            print("Transaction completed.")
            return money
        elif keep_dupes_or_not == "duplicates":
            for item, amount in list(inventory.items()):
                for count in range(amount):
                    while count < amount - 1:
                        if item in SELL_VALUES:
                            money = money + SELL_VALUES.get(item)
                        break
                    inventory[item] = 1
            print("Transaction completed.")
            return money
        elif keep_dupes_or_not == "quit":
            break
        else:
            print("Sorry what you entered isn't an action, please try again")

def buying(inventory, money):
    while True:
        DEFAULT_SHOP_INVENTORY = {
            "iron fishing rod" : 50,
            "spooky fishing rod" : 100,
            "horrifying fishing rod" : 500
            }
        shop_inventory = DEFAULT_SHOP_INVENTORY
        for item in list(DEFAULT_SHOP_INVENTORY.keys()):
            if item in inventory.keys():
                shop_inventory.pop(item)
        print("Here is what we have today.")
        for item, item_price in shop_inventory.items():
            print(f"A {item} for {item_price} coins.")
        item_to_buy = input("What would you like to buy? ").lower()
        if item_to_buy in shop_inventory:
            if money >= shop_inventory.get(item_to_buy):
                user_can_buy = True
            else:
                print("Sorry you don't have enough money for this.")
                continue
            confirmation = input(f'Are you sure you would like to buy a {item_to_buy} for {shop_inventory.get(item_to_buy)} coins? Type "yes" to confirm your choice. ').lower()
            if confirmation == "yes" and user_can_buy:
                money = money - shop_inventory.get(item_to_buy)
                inventory[item_to_buy] = 1
                print(f'Thank you for your purchase of a {item_to_buy}, your current balance is {money} coins.')
                return money
        elif item_to_buy == "quit":
            break
        else:
            print("What you entered isn't an item. Try again.")

def print_inventory(inventory):
    for item, item_amount in inventory.items():
        print(f"{item} x {item_amount}")

def fishing(inventory, available_fish, difficulty):  
    words = f"{difficulty}_words_list"
    words_list = importlib.import_module(words)
    while True:
        print("You cast your line..")
        catch = random.choices(available_fish.keys(), weights=available_fish.values())
        time.sleep(random.randint(3, 5))
        word_to_type = random.choice(words_list.words)
        typed_word = input(f"You feel something pull the line, your word to type is \n{word_to_type} ")
        if typed_word == word_to_type:
            if catch in inventory:
                inventory[catch] = inventory[catch] + 1
            else:
                inventory[catch] = 1
            wants_to_see_inventory = input(f'You caught a {catch}! Press "y" to see your whole inventory, or "quit" to stop fishing. Press enter to fish again. ').lower()
            if wants_to_see_inventory == "y":
                print_inventory(inventory)
                while True:
                    ready_to_catch_more_fish = input("Press enter when you are ready to catch more fish. ")
                    if ready_to_catch_more_fish == "":
                        break
            if wants_to_see_inventory == "quit":
                break
        elif typed_word == "quit":
            break
        else:
            print(f"The {catch} got away.")

def accessing_shop(inventory, money):
    while True:
        buy_or_sell = input("Would you like to buy or sell today? ").lower()
        if buy_or_sell == "buy":
            money = buying(inventory, money)
        elif buy_or_sell == "sell":
            money = selling(inventory, money)
        elif buy_or_sell == "quit":
            return money
        else:
            print("That wasn't a valid action.")

def file_contents_without_newlines(save_slot):
    save_data_contents_without_newline = []
    with open(save_slot) as save_data:
        for line in save_data.readlines():
            line = line.replace("\n", "")
            save_data_contents_without_newline.append(line)
        return save_data_contents_without_newline

def print_each_item_in_list(defined_list):
    for item in defined_list:
        print(item)

def configure_difficulty(difficulty):
    DIFFICULTY_OPTIONS = ["easy", "normal", "hard"]
    print_each_item_in_list(DIFFICULTY_OPTIONS)
    while True:
        new_difficulty = input(f"What would you like to change your difficulty to? It is currently {difficulty}. ").lower()
        if new_difficulty in DIFFICULTY_OPTIONS:
            print(f"Your difficulty has been changed to {new_difficulty}.")
            return new_difficulty
            break
        if new_difficulty == "quit":
            break
        else:
            print("That wasn't a difficulty option.")
            continue

def make_save_slot_active(target_save_slot):
    # This will make one save slot active while also making another inactive if it is active.
    for save_slot in os.listdir():
        if not os.path.isdir(save_slot) and save_slot != "template.py":
            save_data_contents_without_newline = file_contents_without_newlines(save_slot)
            if "active = True" in save_data_contents_without_newline:
                save_data_contents_without_newline.remove("active = True")
                with open(save_slot, "w") as save_data:
                    for line in save_data_contents_without_newline:
                        save_data.write(f"{line}\n")
    with open(f"{target_save_slot}_save_data.py", "a") as save_data:
        save_data.write("active = True")
    print(f"{target_save_slot} will be loaded until you make another slot loaded.")

def check_for_valid_save():
    # This checks for a save slot with "active = True" in the file, and if a file has it the program proceeds as normal
    # If "active = True" is not in any slot it will create a new slot with "active = True" or edit a slot to append "active = True"
    os.chdir("saves")
    for save_slot in os.listdir():
        if save_slot != "template.py" and not os.path.isdir(save_slot):
            if "active = True" in file_contents_without_newlines(save_slot):
                os.chdir(ORIGINAL_WORKING_DIRECTORY)
                return
    save_slot_list = []
    for save_slot in os.listdir():
        if save_slot != "template.py" and not os.path.isdir(save_slot):
            save_slot_list.append(save_slot[: - 13]) # Appends save slot name without _save_data.py
    print_each_item_in_list(save_slot_list)
    save_slot = input("It looks like you don't have any active slots, here is a list of your saves, type the name of a save to make it active. You can also type the name of a new save to create a new, valid one. ")
    if save_slot not in save_slot_list:
        os.chdir(ORIGINAL_WORKING_DIRECTORY)
        create_save_slot(save_slot, active_save = True)
    if save_slot in save_slot_list:
        with open(f"{save_slot}_save_data.py", "a") as save_file:
            save_file.write("active = True")
    os.chdir(ORIGINAL_WORKING_DIRECTORY)

def create_save_slot(new_save_slot, active_save = False):
    os.chdir("saves")
    shutil.copyfile("template.py", f"{new_save_slot}_save_data.py")
    if active_save:
        with open(f"{new_save_slot}_save_data.py", "a") as save_file:
            save_file.write("active = True")
    os.chdir(ORIGINAL_WORKING_DIRECTORY)

def rename_save_slot(save_slot_list, save_slot_to_customize):
    while True:
        new_save_slot_name = input(f"What would you like to rename the save slot {save_slot_to_customize} to? ")
        if new_save_slot_name == "template":
            print("You cannot name a save file that.")
        elif new_save_slot_name == "quit":
            break
        elif new_save_slot_name not in save_slot_list:
            os.rename(f"{save_slot_to_customize}_save_data.py", f"{new_save_slot_name}_save_data.py")
            print(f"Successfully renamed {save_slot_to_customize} to {new_save_slot_name}.")
            return new_save_slot_name
        else:
            print(f"There is already a save slot with the name {new_save_slot_name}.")

def save_data_from_session(inventory, money, available_fish, difficulty, equipment, save_slot):
    os.chdir("saves")
    if "active = True" in file_contents_without_newlines(save_slot):
        active_save_slot = True
    with open(save_slot, "w") as save_file:
        save_file.write(f'inventory = {inventory}\nmoney = {money}\navailable_fish = {available_fish}\ndifficulty = "{difficulty}"\nequipment = {equipment}\n')
        if active_save_slot:
            save_file.write("active = True")
    print("Successfully saved data.")

def save_slot_configuration(active_save_slot):
    while True:
        save_slot_list = []
        for save_slot in os.listdir("saves"):
            if save_slot != "template.py" and not os.path.isdir(save_slot):
                save_slot_list.append(save_slot[: - 13])
        print("Here is a list of your current saves.")
        print_each_item_in_list(save_slot_list)
        while True:
            save_slot_to_customize = input('''What slot would you like customize? You can type the name of a slot that doesn't exist to create one, or "quit" to exit ''')
            if save_slot_to_customize != "template":
                break
            else:
                print("You cannot name a save slot that.")
        if save_slot_to_customize not in save_slot_list and save_slot_to_customize != "quit": 
            create_save_slot(save_slot_to_customize)
            save_slot_list.append(save_slot_to_customize)
            continue
        if save_slot_to_customize == "quit":
            break
        else: # Editing / customizing slots
            AVAILABLE_SLOT_ACTIONS = ["delete", "rename", "make active"]
            print_each_item_in_list(AVAILABLE_SLOT_ACTIONS)
            os.chdir("saves")
            while True:
                action = input(f"What action would you like to do on {save_slot_to_customize}? ")
                if action == "delete":
                    confirmation = input(f'Are you sure you would like to delete {save_slot_to_customize}? Type "yes" to confirm. This will also quit the program so the save slot cannot be remade when you save, assuming you are trying to delete the last loaded slot. ')
                    if confirmation == "yes":
                        os.remove(f"{save_slot_to_customize}_save_data.py")
                        print(f"The slot {save_slot_to_customize} has been successfully deleted. ")
                        if f"{save_slot_to_customize}_save_data.py" == active_save_slot:
                            print("Exiting the program because the active save slot was deleted.")
                            raise SystemExit()
                        else:
                            print("Returning")
                            break
                    else:
                        print("Returning.")
                elif action == "rename":
                    save_slot_to_customize = rename_save_slot(save_slot_list, save_slot_to_customize)
                elif action == "make active":
                    confirmation = input('This will make this save file loaded when you run the program. If multiple save slots will be active, it will overwrite the preexisting save slots status. Types "yes" to confirm. ')
                    if confirmation == "yes":
                        make_save_slot_active(save_slot_to_customize)
                    else:
                        break
                elif action == "quit":
                    break
                else:
                    print("That wasn't an action.")
            os.chdir(ORIGINAL_WORKING_DIRECTORY)

def load_inital_save_data():
    save_data = ""
    save_data_contents_without_newline = []
    os.chdir("saves")
    for save_slot in os.listdir():
        if not os.path.isdir(save_slot) and save_slot !="template.py":
            if "active = True" in file_contents_without_newlines(save_slot):
                sys.path.append(os.getcwd())
                save_slot_without_extension = save_slot.replace(".py", "")
                save_data = importlib.import_module(save_slot_without_extension)
                os.chdir(ORIGINAL_WORKING_DIRECTORY)
                return save_data, save_slot

def edit_equipment(equipment, inventory):
    print("Here is a list of your currently equipped equipment.")
    for equipment_type, equipped_equipment in equipment.items():
        print(f"{equipment_type} = {equipped_equipment}")
    while True:
        equipment_to_change = input("What equipment type would you like to change? ").lower()
        if equipment_to_change == "fishing rod":
            edit_fishing_rod(equipment, inventory)
            return

def edit_fishing_rod(equipment, inventory):
    print("Here is a list of fishing rods in your inventory")
    for item in inventory:
        if "fishing rod" in item:
            print(item)
    while True:
        new_fishing_rod = input("What fishing rod would you like to equip? ").lower()
        if new_fishing_rod in inventory:
            equipment["Fishing Rod"] = new_fishing_rod
            print("Successfully changed equipment.")
            return

check_for_valid_save()
save_data, save_slot = load_inital_save_data()
main(save_data.inventory, save_data.money, save_data.available_fish, save_data.difficulty, save_data.equipment, save_slot)