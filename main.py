import random
import json
from time import sleep
from normal_words_list import words
from stored_save_data import save_data, inventory, user_save_slots


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
                break
        elif action == "view wallet":
            print(save_data["money"])
        elif action == "view inventory":
            print_inventory(inventory)
        elif action == "shop":
            accessing_shop(inventory, save_data)
        elif action == "fish":
            fishing(inventory, save_data)
        elif action == "save data":
            save_data_from_session(inventory, save_data)
        elif action == "customize saves":
            save_slot_customization(user_save_slots)
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
        if keep_dupes_or_not == "quit":
            break
        elif keep_dupes_or_not == "everything":
            for item, amount in list(inventory.items()):
                if item in SELL_VALUES:
                    for count in range(amount):
                        save_data["money"] = save_data["money"] + SELL_VALUES.get(item)
                    del inventory[item]
            print("Transaction completed.")
        elif keep_dupes_or_not == "duplicates":
            for item, amount in list(inventory.items()):
                for count in range(amount):
                    while count < amount - 1:
                        if item in SELL_VALUES:
                            save_data["money"] = save_data["money"] + SELL_VALUES.get(item)
                        break
                    inventory[item] = 1
            print("Transaction completed.")
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
                break
            confirmation = input(f'Are you would like to buy a {choice_to_buy}? Type "yes" to confirm your choice. ').lower()
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
        sleep(random.randint(3, 5))
        word_to_type = random.choice(words)
        typed_word = input(f"You feel something pull the line, quick! your word to type is \n{word_to_type} ")
        if typed_word == word_to_type:
            if catch in inventory:
                inventory[catch] = inventory[catch] + 1
            else:
                inventory[catch] = 1
            wants_to_see_inv = input(f"You caught a {catch}! Press y to see your whole inventory, or anything else to continue. ").lower()
            if wants_to_see_inv == "y":
                print_inventory(inventory)
                while True:
                    ready_to_catch_more_fish = input("Press enter when you are ready to catch more fish.")
                    if ready_to_catch_more_fish == "":
                        break
            if wants_to_see_inv == "quit":
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

def save_data_from_session(inventory, save_data):
    save_data_store = open("stored_save_data.py", "w")
    save_data_store.write(f"inventory = {json.dumps(inventory)}")
    save_data_store.write(f"\nsave_data = {json.dumps(save_data)}")
    save_data_store.write(f"\nuser_save_slots = {json.dumps(user_save_slots)}")
    print("Data stored!")

def save_slot_customization(user_save_slots):
    while True:
        AVAILABLE_SLOT_ACTIONS = ["delete", "rename"]
        print("Here is a list of your current saves.")
        user_save_slots.sort()
        for save in user_save_slots:
            print(save)
        slot_to_customize = input('''What slot would you like customize? You can type the name of a slot that doesn't exist to create one. or "quit" to exit''')
        if slot_to_customize not in user_save_slots and slot_to_customize != "quit":
            user_save_slots.append(slot_to_customize)
        elif slot_to_customize == "quit":
            break
        else:
            while True:
                print("Here is a list of slots you can edit, which one would you like to edit?")
                for save in user_save_slots:
                    print(save)
                slot_being_edited = input()
                if slot_being_edited not in user_save_slots:
                    print("What you entered isn't a slot.")
                    continue
                if slot_being_edited != "quit":
                    print("What would you like to do to the slot? Below is a list of actions.")
                    for slot_action in AVAILABLE_SLOT_ACTIONS:
                        print(slot_action)
                    action = input()
                    
                else:
                    break

main(inventory, save_data)
# testing testing 123