import modules.utils as utils
import os
import contextlib
import logging
import json

def manage_saves(player):
    while True:
        save_list = get_saves()
        action = get_save_action()
        utils.clear()
        if action == "rename a save":
            rename_save_slot(save_list, player)
        elif action == "delete a save":
            delete_save_slot(save_list)
        elif action == "create a save":
            create_save_slot(save_list)
        elif action == "list saves":
            list_saves()
        elif action == "quit":
            return

def get_save_action():
    VALID_ACTIONS = ("rename a save", "delete a save", "create a save", "list saves", "quit" )
    while True:
        print("What action would you like to do? Here is a list of all actions, please type it exactly as shown.")
        for action in VALID_ACTIONS:
            print(action)
        action = input().strip().lower()
        if action not in VALID_ACTIONS:
            utils.clear()
            print("Looks like that wasn't a valid option, do you want to retry?")
            continue
        return action

def rename_save_slot(save_list, player):
    slot_to_rename = select_save_slot(action = "rename", save_list = save_list)
    while True:
        new_name = input(f"What would you like to rename {slot_to_rename} to? If you change your mind you can type 'quit' to quit. ").strip()
        utils.clear()
        if new_name in save_list:
            print(f"You already have a save named {slot_to_rename}, please make another name. ")
            continue
        if new_name == "quit":
            return
        with(contextlib.chdir("saves")):
            os.rename(f"{slot_to_rename}.json", f"{new_name}.json")
        logging.info(f"Renamed the save file {slot_to_rename} to {new_name}")
        return

def delete_save_slot(save_list):
    save_to_delete = select_save_slot(action = "delete", save_list = save_list)
    confirm = input(f"Are you sure you would like to permanently delete {save_to_delete}? Please type 'y' to confirm. ")
    utils.clear()
    if confirm != "y":
        print("Save has not been deleted")
        return
    with (contextlib.chdir("saves")):
        os.remove(f"{save_to_delete}.json")
        print("Save has been deleted, please keep in mind the save will be remade if you save your data again.")
    return

def create_save_slot(save_list):
    while True:
        new_save = input("Type a new save name to make a slot, or type 'quit' to quit. ").strip()
        utils.clear()
        if new_save in save_list:
            print(f"You already have a save named {new_save}. Try a new name.")
            continue
        if new_save == "quit":
            return
        with(contextlib.chdir("saves")):
            with(open(f"{new_save}.json", "a")) as new_save:
                logging.info(f"Made a new save, {new_save}")
                return

def get_active_save():
    utils.clear()
    if not os.path.exists("saves"):
        os.mkdir("saves")
    save_list = get_saves()
    if len(save_list) == 0:
        return None
    if len(save_list) == 1:
        return save_list[0]
    selected_save = select_save_slot(action = "continue", save_list = save_list)
    return selected_save

def list_saves():
    for save in os.listdir("saves"):
        print(save)

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
        utils.clear()
        if selected_save not in save_list:
            print("That wasn't a valid choice, please try again.")
            continue
        return selected_save

def save_data(player):
    save_list = get_saves()
    if len(save_list) == 0:
        print("Looks like you don't have any saves, please make a save by managing your saves to continue.")
        return
    else:
        save_to_write = select_save_slot(action = "continue", save_list = save_list)
    with contextlib.chdir("saves"):
        with open(f"{save_to_write}.json", "w") as save_data:
            json.dump(player.__dict__, save_data, indent = 4)
        logging.info(f"Saved data in {os.getcwd()} as {save_to_write}.json")  
    print("Data saved")