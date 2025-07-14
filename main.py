import random
import save_data

def main():
    ACTION_LIST = ["fish"]
    add_to_inventory("carp")
def fish():
    AVAILABLE_FISHES = ["carp", "salmon", "crabfish"]
    catch = random.choice(AVAILABLE_FISHES)

def add_to_inventory(item):
    inventory = save_data.data["inventory"]
    try:
        inventory[item] += 1
    except KeyError:
        inventory[item] = 1
    save_data.data["inventory"] = inventory

if __name__ == "__main__":
    main()