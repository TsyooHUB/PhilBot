import os.path

philbank = []


class Register:
    def __init__(self, name, user_id, balance):
        self.name = name
        self.user_id = user_id
        self.balance = balance

    def set_name(self, name):
        self.name = name

    def set_id(self, user_id):
        self.user_id = user_id

    def set_balance(self, balance):
        self.balance = balance

    def get_name(self):
        return self.name

    def get_id(self):
        return self.user_id

    def get_balance(self):
        return self.balance


def add_philcoin(user_id, name, amount):
    for register in philbank:
        if user_id == register.get_id():
            register.set_name(name)
            register.set_balance(register.get_balance()+int(amount))
            save_philbank()
            return
    new_register = Register(name, user_id, amount)
    philbank.append(new_register)
    save_philbank()


def get_philcoin_balance(user_id):
    for register in philbank:
        if str(user_id) == register.get_id():
            return register.get_balance()
    return -1


def save_philbank():
    with open('data/philbank.txt', 'w') as f:
        for register in philbank:
            f.write("{'Name': '" + str(register.get_name()) + "','UserId': " + str(register.get_id())
                    + ",'Balance': " + str(register.get_balance()) + "}\n")


def start_bank():
    if not os.path.exists('data/philbank.txt'):
        open('data/philbank.txt', 'w')

    with open("data/philbank.txt", "r") as f:
        for line in f:
            new_register = eval(line)
            philbank.append(Register(str(new_register.get("Name")), str(new_register.get('UserId')),
                                     str(new_register.get('Balance'))))

    return "PhilBank opened successfully"
