import random
import os
import sys
import importlib
import time
import shutil
from normal_words_list import words
ORIGINAL_WORKING_DIRECTORY = os.getcwd()
def main(inventory, save_data):
    last_action = "save data"
    while True:
        AVAILABLE_ACTIONS = ["help", "fish", "shop", "quit", "view wallet", "view inventory", "save data", "customize saves", "configure settings",]
        action = input('What would you like to do? Type "help" for a list of actions, and as a reminder, you can type "quit" at any time to go back to the previous menu. ').lower()
        if action == "help":
            print(f"Here is a list of available actions")
            AVAILABLE_ACTIONS.sort()
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
            accessing_shop(inventory, money)
        elif action == "fish":
            fishing(inventory, money)
        elif action == "save data":
            save_data_from_session(inventory, money, save_slot)
        elif action == "customize saves":
            save_slot_customization()
        else:
            print("What you entered isn't a valid action, please try again.")
        if action in AVAILABLE_ACTIONS and action != "quit":
            last_action = action

def selling(inventory, save_data):
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
            break
        elif keep_dupes_or_not == "duplicates":
            for item, amount in list(inventory.items()):
                for count in range(amount):
                    while count < amount - 1:
                        if item in SELL_VALUES:
                            money = money + SELL_VALUES.get(item)
                        break
                    inventory[item] = 1
            print("Transaction completed.")
            break
        elif keep_dupes_or_not == "quit":
            break
        else:
            print("Sorry what you entered isn't an action, please try again")

def buying(inventory, save_data):
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
                break
        elif item_to_buy == "quit":
            break
        else:
            print("What you entered isn't an item. Try again.")

def print_inventory(inventory):
    for item, item_amount in inventory.items():
        print(f"{item} x {item_amount}")

def fishing(inventory, save_data):  
    while True:
        print("You cast your line..")
        catch = random.choice(save_data["available_fish"])
        time.sleep(random.randint(3, 5))
        word_to_type = random.choice(words)
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

def accessing_shop(inventory, save_data):
    while True:
        buy_or_sell = input("Would you like to buy or sell today? ").lower()
        if buy_or_sell == "buy":
            buying(inventory, save_data)
        elif buy_or_sell == "sell":
            selling(inventory, save_data)
        elif buy_or_sell == "quit":
            break
        else:
            print("That wasn't a valid action.")

def save_data_from_session(inventory, save_data, save_slot):
    os.chdir("saves")
    with open(save_slot, "w") as save_file:
        save_file.write(f"inventory = {inventory}\nsave_data.money = {money}\n")
        if "active = True" in file_contents_without_newlines(save_slot):
            save_file.write("active = True")
    print("Successfully saved data.")

def save_slot_customization():
    save_slot_list = []
    for save_slot in os.listdir("saves"):
        if save_slot != "template.py" and not os.path.isdir(save_slot):
            save_slot_list.append(save_slot[: - 20])
    while True:
        print("Here is a list of your current saves.")
        print_each_item_in_list(save_slot_list)
        save_slot_to_customize = input('''What slot would you like customize? You can type the name of a slot that doesn't exist to create one, or "quit" to exit ''')
        if save_slot_to_customize not in save_slot_list and save_slot_to_customize != "quit": 
            create_save_slot(save_slot_to_customize)
            save_slot_list.append(save_slot_to_customize)
        if save_slot_to_customize == "quit":
            break
        else: # Editing / customizing slots
            AVAILABLE_SLOT_ACTIONS = ["delete", "rename", "make active"]
            print_each_item_in_list(AVAILABLE_SLOT_ACTIONS)
            os.chdir("saves")
            while True:
                action = input(f"What action would you like to do on {save_slot_to_customize}? ")
                if action == "delete":
                    confirmation = input(f'Are you sure you would like to delete {save_slot_to_customize}? Type "yes" to confirm. ')
                    if confirmation == "yes":
                        os.remove(f"{save_slot_to_customize}_save_data.py")
                        print(f"The slot {save_slot_to_customize} has been successfully deleted. ")
                        break
                    else:
                        print("Returning.")
                elif action == "rename":
                    rename_save_slot(save_slot_list, save_slot_to_customize)
                elif action == "make active":
                    confirmation = input('This will make this save file loaded when you run the program. If multiple save slots will be active, it will overwrite the preexisting save slots status. Types "yes" to confirm. ')
                    if confirmation == "yes":
                        make_save_slot_active()
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

def file_contents_without_newlines(save_slot):
    save_data_contents_without_newline = []
    with open(save_slot) as save_data:
        for line in save_data.readlines():
            line = line.replace("\n", "")
            save_data_contents_without_newline.append(line)
        return save_data_contents_without_newline

def make_save_slot_active():
    for save_slot in os.listdir():
        if not os.path.isdir(save_slot) and save_slot != "template.py":
            save_data_contents_without_newline = file_contents_without_newlines(save_slot)
            if "active = True" in save_data_contents_without_newline:
                save_data_contents_without_newline.remove("active = True")
                with open(save_slot, "w") as save_data:
                    for line in save_data_contents_without_newline:
                        save_data.write(f"{line}\n")
    with open(f"{save_slot_to_customize}_save_data.py", "a") as save_data:
        save_data.write("active = True")
    print(f"{save_slot_to_customize} will be loaded until you make another slot loaded.")

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
            save_slot_list.append(save_slot[: -20])
    for save_slot in save_slot_list:
        print(save_slot)
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
    new_file_name = input(f"What would you like to rename the save slot {save_slot_to_customize} to? ")
    while True:
        if new_file_name == "quit":
            print("Returning.")
            return
        elif new_file_name not in save_slot_list:
            os.rename(f"{save_slot_to_customize}_save_data.py", f"{new_slot_name}_save_data.py")
            print(f"Successfully renamed {save_slot_to_customize} to {new_slot_name}.")
            return
        else:
            print(f"There is already a save slot with the name {new_save_slot_name}.")

def print_each_item_in_list(defined_list):
    for item in defined_list:
        print(item)

def configure_difficulty():
    DIFFICULTY_OPTIONS = ["easy", "medium", "hard"]
    new_difficulty = input("What would you like to change your difficulty to? It is currently {difficulty}. ")
    print_each_item_in_list(DIFFICULTY_OPTIONS)

def configure_settings():
    CONFIGURATION_CHOICES = ["difficulty",]
    while True:
        configuration_choice = input("What would you like to configure? ")
        print_each_item_in_list(CONFIGURATION_CHOICES)
        if configuration_choice in CONFIGURATION_CHOICES:
            if configuration_choice == "difficulty":
                configure_difficulty()
        else:
            print("That wasn't a valid configuration option")

check_for_valid_save()
save_data, save_slot = load_inital_save_data()
main(inventory, save_data)