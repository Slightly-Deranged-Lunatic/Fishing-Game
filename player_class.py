class Player:
    def __init__(self, name, money, inventory):
        self.name = name
        self.money = money
        self.inventory = inventory

    def show_inventory(self):
        for item, amount in self.inventory.items():
            print(f"{item} x {amount}")
