class Player:
    def __init__(self, name, money, inventory, save):
        self.name = name
        self.money = money
        self.inventory = inventory
        self.save = save
    def show_inventory(self):
        for item, amount in self.inventory.items():
            print(f"{item} x {amount}")
