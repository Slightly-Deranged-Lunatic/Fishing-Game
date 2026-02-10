class Player:
    def __init__(self, money, inventory):
        self._money = money
        self._inventory = inventory

    def get_money(self):
        return self._money

    def set_money(self, new_money):
        self._money = new_money

    money = property(get_money, set_money)

    def get_inventory(self):
        return self._inventory

    def set_inventory(self, new_inventory):
        self._inventory = new_inventory

    inventory = property(get_inventory, set_inventory)

    def show_inventory(self):
        for item, amount in self._inventory.items():
            print(f"{item} x {amount}")

    def show_money(self):
        print(f"Player has {self.money} dollars.")