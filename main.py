import contextlib
import os
import datetime
import time
import random
import logging
import json

if not os.path.exists("Logs"):
    os.mkdir("Logs")

logging.basicConfig(
    filename = f"Logs/{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log",
    encoding = "utf-8",
    filemode = "w",
    format = "{asctime} - {levelname} - {message}",
    style = "{",
    level = logging.INFO
)

def main():
    clear_logs()
    VALID_ACTIONS = ["fish", "shop", "view inventory"]
    FUNCTION_MAP = {
        "fish": fish,
        "shop": shop,
        "view inventory" : view_inventory
    }
    while True:
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
    ENDCOLOR = "\033[m"
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
            print("Looks like that wasn't an option, did you make a typo?")
            clear()

def sell():
    item_prices = load_json(os.getcwd(), "item_prices.json")
    sell_values = item_prices["sell_price"]
    print("Selling your inventory")
    money_made = 0
    for item, amount in player_data["inventory"].items():
        money_made += sell_values[item] * amount
    player_data["money"] += money_made
    print(f"You have {player_data["money"]} dollars and you made {money_made} dollars.")
    
    player_data["inventory"].clear()

def buy():
    print("Well there ain't much here yet so maybe check back later...")

def clear_logs():
    # Clears all but 5 most recent logs
    with(contextlib.chdir("Logs")):
        files = os.listdir()
        files.sort()
        files.reverse()
        LOGS_TO_REMOVE = files[5:]
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
    except NotADirectoryError:
        logging.critical(f"{path} was not a directory when trying to load json {json_name}!")
    except FileNotFoundError:
        logging.critical(f"Json {json_name} was not found in {path}, does it exist?")
    except:
        logging.critical(f"Error when trying to load JSON {json_name}")
    return json_data

def add_to_inventory(item):
    if item not in player_data["inventory"]:
        player_data["inventory"] = 1
    else:
        player_data["inventory"] += 1

def view_inventory():
    for item in player_data["inventory"]:
        print(item)

if __name__ == "__main__":
    player_data = load_json(os.getcwd(), "player.json")
    main()