import os
import contextlib
import logging
import json

import modules.saves as saves

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
                return json_data
    except:
        logging.exception("Error occured while trying to load json! Program is gonna crash anyways so uhm")
        raise SystemExit