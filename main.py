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
    filename=f"Logs/{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log",
    encoding="utf-8",
    filemode="w",
    format="{asctime} - {levelname} - {message}",
    style="{",
    level=logging.INFO
)

def main():
    clear_logs()
    fish()

def fish():
    WORD_TO_TYPE_COLOR = "\033[35m" # A magenta ish color
    ENDCOLOR = "\033[m"
    logging.info("User went fishing.")

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
        print(f"You got a {caught_fish}")
    return

def clear_logs():
    # Clears all but 5 most recent logs
    with(contextlib.chdir("Logs")):
        files = os.listdir()
        files.sort()
        files.reverse()
        FILES_TO_REMOVE = files[5:]
        for file in FILES_TO_REMOVE:
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
        logging.critical(f"{path} was not a directory when trying to load json!")
    except:
        logging.critical(f"Error when trying to load JSON {json_name}")
    return json_data
if __name__ == "__main__":
    main()