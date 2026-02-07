import contextlib
import os
import datetime
import time
import random
import logging
import json
from player_class import Player

if not os.path.exists("logs"):
    os.mkdir("logs")

logging.basicConfig(
    filename = f"logs/{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log",
    encoding = "utf-8",
    filemode = "w",
    format = "{asctime} - {levelname} - {message}",
    style = "{",
    level = logging.INFO
)

def main():
    FUNCTION_MAP = {
        "fish": fish,
        "shop": shop,
        "view inventory": view_inventory,
        "save": save_data,
        "quit": stop_playing,
        "manage saves": manage_saves
    }
    VALID_ACTIONS = list(FUNCTION_MAP.keys())

    while True:
        clear()
        print("What would you like to do?")
        for i in VALID_ACTIONS:
            print(i)
        action = input("Please type it exactly as you see above: ").strip().lower()
        if action not in VALID_ACTIONS:
            clear()
            print("It looks like you made a typo somewhere.")
            continue
        function_to_do = FUNCTION_MAP.get(action)
        clear()
        function_to_do()

def fish():
    WORD_TO_TYPE_COLOR = "\033[35m" # A magenta ish color
    ENDCOLOR = "\033[m" # Removes the color
    logging.info("User went fishing.")
    while True:
        print("You cast your line")
        word_to_type = random.choice(load_json("words_lists", "default.json")["words"])
        time.sleep(random.randint(2, 4))
        clear()
        typed_word = input(f"Type the word '{WORD_TO_TYPE_COLOR}{word_to_type}{ENDCOLOR}' to catch the fish! ")
        
        if typed_word != word_to_type:
            print("The fish got away! Oh no!")
        else:
            fish_list = (load_json(os.getcwd(), "fish_list.json"))
            caught_fish = random.choice(fish_list["fish"])
            logging.info(f"User caught a {caught_fish}")
            print(f"You got a {caught_fish}")
            add_to_inventory(caught_fish)
            user_done = input("Press enter to catch more fish, or type 'done' to leave. ").strip().lower()
        if user_done != "done":
            clear()
            continue
        else:
            return

def shop():
    logging.info("User went to the shop")
    SHOP_MESSAGE = """Welcome to the shop!
Would you like to buy or sell today? You can also type 'done' to leave the shop. """
    while True:
        action = input(SHOP_MESSAGE).strip().lower()
        if action == "sell":
            sell()
        elif action == "buy":
            buy()
        elif action == "done":
            return
        else:
            clear()
            print("Looks like that wasn't an option, did you make a typo?")

def sell():
    logging.info("User went to sell stuff")
    item_prices = load_json(os.getcwd(), "item_prices.json")
    sell_values = item_prices["sell_price"]
    print("Selling your inventory")
    money_made = 0
    for item, amount in player.inventory.items():
        money_made += sell_values[item] * amount
    player.money += money_made
    print(f"You have {player.money} dollars and you made {money_made} dollars.")
    player.inventory.clear()
    input("Press enter when you are ready to go back to the shop.")
    clear()

def buy():
    logging.info("User tried to buy something... What a noob")
    print("Well there ain't much here yet so maybe check back later...")

def clear_logs():
    # Clears all but 5 most recent logs
    files = os.listdir("logs")
    files.sort()
    files.reverse()
    LOGS_TO_REMOVE = files[5:]
    with(contextlib.chdir("logs")):
        for file in LOGS_TO_REMOVE:
            os.remove(file)
        logging.info("Logs cleaned")

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def load_json(path, json_name):
    try:
        with(contextlib.chdir(path)):
            logging.info(f"Currently in {os.getcwd()}")
            with(open(json_name)) as data:
                json_data = json.load(data)
        error = False
    except NotADirectoryError:
        error = True
        logging.exception(f"{path} was not a directory when trying to load json {json_name}!")
    except FileNotFoundError:
        error = True
        logging.exception(f"Json {json_name} was not found in {path}, does it exist?")
    except:
        error = True
        logging.exception(f"Error when trying to load JSON {json_name}")
    if error:
        json_data = None
    else:
        return json_data

def add_to_inventory(item):
    if item not in player.inventory:
        player.inventory[item] = 1
    else:
        player.inventory[item] += 1

def view_inventory():
    print("Here is your inventory:")
    player.show_inventory()
    input("Press enter when you are ready to go back to the main menu.")
    clear()

def stop_playing():
    print("Bye bye!")
    raise SystemExit

def save_data():
    logging.info("User saving data.")
    if player.save == None:
        player.save = "New Save"
    with contextlib.chdir("saves"):
        with open(f"{player.save}.json", "w") as save_data:
            json.dump(player.__dict__, save_data, indent = 4)
        logging.info(f"Saved data in {os.getcwd()} as {player.save}.json")

def load_player_data():
    logging.info("Trying to get player data")
    player = Player(name = "default", money = 0, inventory = {}, save = get_active_slot())
    try:
        logging.info(f"Player save is {player.save}")
        if player.save == None:
            logging.info("Save slot was None, raising FileNotFoundError")
            raise FileNotFoundError
        player_save = load_json("saves", f"{player.save}.json")
        name = player_save["name"]
        money = player_save["money"]
        inventory = player_save["inventory"]
        save = player.save
        player = Player(name, money, inventory, save) # player instance is remade because its more readable than direct assignment
        logging.info("Found player data")
    except:
        logging.exception("Something went wrong while trying to load data!")
        
    return player

def manage_saves():
    FUNCTION_MAP = {
        "rename": rename_save_slot,
        "delete": delete_save_slot,
        "create a slot": create_save_slot,
        "list saves": list_saves
    }
    VALID_ACTIONS = list(FUNCTION_MAP.keys())
    VALID_ACTIONS.append("quit")
    while True:
        save_list = get_saves()
        print("What action would you like to do? Here is a list of all actions, please type it exactly as shown.")
        for action in VALID_ACTIONS:
            print(action)
        selected_action = input().strip().lower()
        if selected_action not in VALID_ACTIONS:
            print("Please try again")
            clear()
            continue
        if selected_action == "quit":
            return
        function_to_do = FUNCTION_MAP.get(selected_action)
        clear()
        function_to_do(save_list)

def rename_save_slot(save_list):
    slot_to_rename = select_save_slot(action = "rename", save_list = save_list)
    while True:
        new_name = input(f"What would you like to rename {slot_to_rename} to? If you change your mind you can type 'quit' to quit. ").strip()
        if new_name in save_list:
            print(f"You already have a slot named {slot_to_rename}, please make another name. ")
            continue
        if new_name == "quit":
            return
        with(contextlib.chdir("saves")):
            os.rename(f"{slot_to_rename}.json", f"{new_name}.json")
        logging.info(f"Renamed the save file {slot_to_rename} to {new_name}")
        player.save = new_name
        return

def delete_save_slot(save_list):
    save_to_delete = select_save_slot(action = "delete", save_list = save_list)
    confirm = input(f"Are you sure you would like to permanently delete {save_to_delete}? Please type 'y' to confirm. ")
    if confirm != "y":
        print("Very well")
        return
    with (contextlib.chdir("saves")):
        os.remove(f"{save_to_delete}.json")
    return

def create_save_slot(save_list):
    while True:
        new_save = input("Type a new slot name to make a slot.")
        if new_save in save_list:
            print(f"You already have a slot named {new_save}. Try a new name.")
        with(open(f"{new_save}.json", "a")) as new_save:
            logging.info(f"Made a new save, {new_save}")
            return

def list_saves():
    for save in os.listdir("saves"):
        print(save.removesuffix(".json"))

def get_active_slot():
    clear()
    if not os.path.exists("saves"):
        os.mkdir("saves")
    saves = get_saves()
    if len(saves) == 0:
        return None
    if len(saves) == 1:
        return saves[0]
    print("It looks like you have more than 1 save slot, please type in a save to continue.")
    while True:
        list_saves()
        selected_save = input()
        if selected_save not in saves:
            clear()
            print("Looks like that wasn't a slot, please try again.")
            continue
        return selected_save

def get_saves():
    save_list = os.listdir("saves")
    save_list_without_suffix = list()
    for save in save_list:
        save_list_without_suffix.append(save.removesuffix(".json"))
    return save_list_without_suffix

def select_save_slot(action, save_list):
    while True:
        list_saves()
        selected_save = input(f"Please select a save slot to {action} ").strip()
        if selected_save not in save_list:
            clear()
            print("That wasn't a valid choice, please try again.")
            continue
        clear()
        return selected_save

if __name__ == "__main__":
    clear_logs()
    player = load_player_data()
    main()