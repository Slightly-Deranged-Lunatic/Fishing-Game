import contextlib
import os
import datetime
import time
import random
import logging
import json

from classes.player_class import Player
import modules.saves as saves
import modules.utils as utils

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
    player = load_player_data()

    while True:
        action = get_main_menu_action()
        if action == "fish":
            fish(player)
        if action == "shop":
            shop(player)
        if action == "view inventory":
            view_inventory(player)
        if action == "save":
            saves.save_data(player)
        if action == "quit":
            stop_playing()
        if action == "manage saves":
            saves.manage_saves(player)
        if action == "show money":
            player.show_money()

def get_main_menu_action():
    VALID_ACTIONS = ("fish", "shop", "view inventory", "save", "quit", "manage saves", "show money")
    while True:
        print("What would you like to do?")
        for i in VALID_ACTIONS:
            print(i)
        action = input("Please type it exactly as you see above: ").strip().lower()
        if action not in VALID_ACTIONS:
            utils.clear()
            print("It looks like you made a typo somewhere.")
            continue
        utils.clear()
        return action

def fish(player):
    WORD_TO_TYPE_COLOR = "\033[35m" # A magenta ish color
    ENDCOLOR = "\033[m" # Removes the color
    logging.info("User went fishing.")
    while True:
        print("You cast your line")
        word_to_type = random.choice(utils.load_json("words_lists", "default.json")["words"])
        time.sleep(random.randint(2, 4))
        utils.clear()
        typed_word = input(f"Type the word '{WORD_TO_TYPE_COLOR}{word_to_type}{ENDCOLOR}' to catch the fish! ")
        utils.clear()
        if typed_word != word_to_type:
            print("The fish got away! Oh no!")
        else:
            fish_list = (utils.load_json(os.getcwd(), "fish_list.json"))
            caught_fish = random.choice(fish_list["fish"])
            logging.info(f"User caught a {caught_fish}")
            print(f"You got a {caught_fish}")
            add_to_inventory(caught_fish, player)
            user_done = input("Press enter to catch more fish, or type 'quit' to leave. ").strip().lower()
            utils.clear()
            if user_done != "quit":
                continue
            else:
                return

def shop(player):
    logging.info("User went to the shop")
    SHOP_MESSAGE = """Welcome to the shop!
Would you like to buy or sell today? You can also type 'done' to leave the shop. """
    while True:
        action = input(SHOP_MESSAGE).strip().lower()
        utils.clear()
        if action == "sell":
            sell(player)
        elif action == "buy":
            buy(player)
        elif action == "done":
            return
        else:
            utils.clear()
            print("Looks like that wasn't an option, did you make a typo?")

def sell(player):
    logging.info("User went to sell stuff")
    item_prices = utils.load_json(os.getcwd(), "item_prices.json")
    sell_values = item_prices["sell_price"]
    print("Selling your inventory")
    money_made = 0
    for item, amount in player.inventory.items():
        money_made += sell_values[item] * amount
    player.money += money_made
    print(f"You have {player.money} dollars and you made {money_made} dollars.")
    player.inventory.utils.clear()
    input("Press enter when you are ready to go back to the shop. ")
    utils.clear()

def buy(player):
    logging.info("User tried to buy something... What a noob")
    print("Well there ain't much here yet so maybe check back later...")

def add_to_inventory(item, player):
    if item not in player.inventory:
        player.inventory[item] = 1
    else:
        player.inventory[item] += 1

def view_inventory(player):
    print("Here is your inventory:")
    player.show_inventory()
    input("Press enter when you are ready to go back to the main menu. ")
    utils.clear()

def stop_playing():
    print("Bye bye!")
    raise SystemExit

def load_player_data():
    logging.info("Trying to get player data")
    player = Player(money = 0, inventory = {})
    player_selected_save = saves.get_active_save()
    try:
        if player_selected_save == None:
            logging.info("No save file found")
            raise FileNotFoundError
        player_save = utils.load_json("saves", f"{player_selected_save}.json")
        money = player_save["_money"]
        inventory = player_save["_inventory"]
        player = Player( money, inventory) # player instance is remade because its more readable than direct assignment
        logging.info("Found player data")
    except FileNotFoundError:
        logging.info(f"Using default player values due to no save file, save files are {saves.get_saves()}")
    except:
        logging.exception("Something went wrong while trying to load data!")
        
    return player

if __name__ == "__main__":
    utils.clear_logs()
    main()
