import os
import contextlib
import logging
import json
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