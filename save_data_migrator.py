import os
import importlib
import sys
def main():
    os.chdir("saves")
    sys.path.append(os.getcwd())
    for save_file in os.listdir():
        if save_file != "template.py" and not os.path.isdir(save_file):
            print(save_file[: - 20])
    slot_to_migrate = input("What slot would you like to migrate to the new save data system? ")
    all_save_data = importlib.import_module(f"{slot_to_migrate}_stored_save_data")
    with open(f"{slot_to_migrate}_stored_save_data.py") as save_file:
        with open(f"{slot_to_migrate}_save_data.py", "w") as new_save_file:
            new_save_file.write(f"active = {all_save_data.active}\n")
            new_save_file.write(f"inventory = {all_save_data.inventory}\n")
            for data, value in all_save_data.save_data.items():
                new_save_file.write(f"{data} = {value}\n")
    os.remove(f"{slot_to_migrate}_stored_save_data.py")
    print(f"Successfully migrated data, please note that the full name of the save file is {slot_to_migrate}_save_data.py")
main()