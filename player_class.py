class Player:
    def __init__(self, name, money, inventory, save):
        self._name = name
        self._money = money
        self._inventory = inventory
        self._save = save
    
    def get_name(self):
        return self._name

    def set_name(self, new_name):
        self._name = new_name

    name = property(get_name, set_name)

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

    def get_save(self):
        return self._save

    def set_save(self, new_save):
        self._save = new_save
    
    save = property(get_save, set_save)

    def show_inventory(self):
        for item, amount in self._inventory.items():
            print(f"{item} x {amount}")

    def show_money(self):
        print(f"Player has {self.money} dollars.")