import random
import os
import sys
import importlib
import time
import shutil
from normal_words_list import words
original_working_directory = os.getcwd()
def main(inventory, save_data):
    last_action = "save data"
    while True:
        AVAILABLE_ACTIONS = ["help", "fish", "shop", "quit", "view wallet", "view inventory", "save data", "customize saves",]
        action = input('What would you like to do? Type "help" for a list of actions, and as a reminder, you can type "quit" at any time to go back to the previous menu. ').lower()
        if action == "help":
            print(f"Here is a list of available actions")
            AVAILABLE_ACTIONS.sort()
            for action in AVAILABLE_ACTIONS:
                print(action)
        elif action == "quit":
            if last_action != "save data":
                confirm_exit_without_save = input('You are about to quit without saving, type "yes" to confirm you want to do this and anything else to go back to save. ')
            if last_action == "save data" or confirm_exit_without_save == "yes":
                print("Sad to see you go! Goodbye!")
                raise SystemExit()
        elif action == "view wallet":
            print(save_data["money"])
        elif action == "view inventory":
            print_inventory(inventory)
        elif action == "shop":
            accessing_shop(inventory, save_data)
        elif action == "fish":
            fishing(inventory, save_data)
        elif action == "save data":
            save_data_from_session(inventory, save_data, save_slot)
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
                        save_data["money"] = save_data["money"] + SELL_VALUES.get(item)
                    del inventory[item]
            print("Transaction completed.")
            break
        elif keep_dupes_or_not == "duplicates":
            for item, amount in list(inventory.items()):
                for count in range(amount):
                    while count < amount - 1:
                        if item in SELL_VALUES:
                            save_data["money"] = save_data["money"] + SELL_VALUES.get(item)
                        break
                    inventory[item] = 1
            print("Transaction completed.")
            break
        elif keep_dupes_or_not == "quit":
            break
        else:
            print("Sorry what you entered isn't an action, please try again")

def buying(inventory, save_data):
    SHOP_INVENTORY = {
        "iron fishing rod" : 50,
        "spooky fishing rod" : 100,
        "horrifying fishing rod" : 500
        }
    while True:
        print("Here is what we have today.")
        for item, item_price in SHOP_INVENTORY.items():
            print(f"A {item} for {item_price} coins.")
        choice_to_buy = input("What would you like to buy? ").lower()
        if choice_to_buy in SHOP_INVENTORY:
            if save_data["money"] >= SHOP_INVENTORY.get(choice_to_buy):
                user_can_buy = True
            else:
                print("Sorry you don't have enough money for this.")
                continue
            confirmation = input(f'Are you sure you would like to buy a {choice_to_buy} for {SHOP_INVENTORY.get(choice_to_buy)} coins? Type "yes" to confirm your choice. ').lower()
            if confirmation == "yes" and user_can_buy:
                save_data["money"] = save_data["money"] - SHOP_INVENTORY.get(choice_to_buy)
                inventory[choice_to_buy] = 1
                print(f'Thank you for your purchase of a {choice_to_buy}, your current balance is {save_data["money"]} coins.')
                break
        elif choice_to_buy == "quit":
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
        typed_word = input(f"You feel something pull the line, quick! your word to type is \n{word_to_type} ")
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
    with open(save_slot, "w+") as save_file:
        save_file.write(f"inventory = {inventory}\nsave_data = {save_data}\n")
        if "active = True" in save_file.readlines():
            save_file.write("active = True")
    print("Successfully saved data.")

def save_slot_customization():
    user_save_slots = []
    print(os.getcwd())
    for save_slot in os.listdir("saves"):
        if save_slot != "template.py":
            user_save_slots.append(save_slot[: -20])
    while True:
        print("Here is a list of your current saves.")
        for file in os.listdir("saves"):
            if file != "template.py":
                print(file[: -20]) # Prints the word that comes before _stored_save_data.py
        slot_to_customize = input('''What slot would you like customize? You can type the name of a slot that doesn't exist to create one. or "quit" to exit ''')
        if slot_to_customize not in user_save_slots and slot_to_customize != "quit": # Creates a slot
            os.chdir("saves")
            copyfile("template.py", slot_to_customize + "_stored_save_data.py")
            os.chdir(original_working_directory)
        elif slot_to_customize == "quit":
            break
        else: # Editing / customizing slots
            AVAILABLE_SLOT_ACTIONS = ["delete", "rename", "make active"]
            for save_slot_action in AVAILABLE_SLOT_ACTIONS:
                print(save_slot_action)
            os.chdir("saves")
            while True:
                action = input(f"What action would you like to do on {slot_to_customize}? ")
                if action == "delete":
                    confirmation = input(f'Are you sure you would like to delete {slot_to_customize}? Type "yes" to confirm. ')
                    if confirmation == "yes":
                        os.remove(f"{slot_to_customize}_stored_save_data.py")
                        print(f"The slot {slot_to_customize} has been successfully deleted. ")
                        break
                    else:
                        print("Returning.")
                elif action == "rename":
                    new_file_name = input("What would you like to rename the file to? ")
                    slot_to_customize = slot_to_customize + "_stored_save_data.py"
                    new_file_name = new_file_name + "_stored_save_data.py"
                    if new_file_name not in os.listdir():
                        os.rename(slot_to_customize, new_file_name)
                    else:
                        print("That file already exists.")
                    break
                elif action == "make active":
                    confirmation = input('This will make this save file loaded when you run the program. If multiple save slots will be active, it will overwrite the preexisting save slots status ')
                    if confirmation == "yes":
                        save_data_contents_without_newline = []
                        for save_slot in os.listdir():
                            if not os.path.isdir(save_slot) and save_slot != "template.py":
                                with open(save_slot, "r") as save_data:
                                    save_data_contents = save_data.readlines()
                                    for content in save_data_contents:
                                        content = content.replace("\n", "")
                                        save_data_contents_without_newline.append(content)
                                    if "active = True" in save_data_contents_without_newline:
                                        save_data_contents_without_newline.remove("active = True")
                                with open(save_slot, "w") as save_data:
                                    for content in save_data_contents_without_newline:
                                        print(content)
                                        save_data.write(f"{content}\n")

                        print("File has been made default.")
                    else:
                        print("Returning.")
                        break
                elif action == "quit":
                    break
                else:
                    print("That wasn't an action.")
            os.chdir(original_working_directory)

def check_for_valid_save():
    user_save_slots = []
    for save_slot in os.listdir("saves"):
        if save_slot != "__pycache__" and save_slot != "template.py":
            user_save_slots.append(save_slot)
    if user_save_slots == []:
        new_save_slot = input("It looks like you don't have any saves. This could be because you messed up or this is your first run. Type a name to create a new save file. ")
        os.chdir("saves")
        shutil.copyfile("template.py", f"{new_save_slot}_stored_save_data.py")
        os.chdir(original_working_directory)

def load_inital_save_data():
    all_save_data = ""
    save_data_contents_without_newline = []
    os.chdir("saves")
    for save_slot in os.listdir():
        if not os.path.isdir(save_slot) and save_slot !="template.py":
            with open(save_slot) as save_data:
                save_data_contents = save_data.readlines()
                for content in save_data_contents:
                    content = content.replace("\n", "")
                    save_data_contents_without_newline.append(content)
                if "active = True" in save_data_contents_without_newline:
                    sys.path.append(os.getcwd())
                    save_slot = save_slot.replace(".py", "")
                    all_save_data = importlib.import_module(save_slot)
    os.chdir(original_working_directory)
    return all_save_data, save_slot

check_for_valid_save()
all_save_data, save_slot = load_inital_save_data()
inventory = all_save_data.inventory
save_data = all_save_data.save_data
main(inventory, save_data)