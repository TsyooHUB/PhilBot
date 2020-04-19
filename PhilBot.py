import discord
import os.path

BOT_PREFIX = ("!")
TOKEN = ''

client = discord.Client()
philbank = []


class Register:
    def __init__(self, user_id, balance):
        self.user_id = user_id
        self.balance = balance

    def set_id(self, user_id):
        self.user_id = user_id

    def set_balance(self, balance):
        self.balance = balance

    def get_id(self):
        return self.user_id

    def get_balance(self):
        return self.balance


# not used
def philbank_contains_id(self, id):
    for register in philbank:
        if register.get_id() == id:
            return True
    return False


def add_philcoin(user_id, amount):
    for register in philbank:
        if user_id == register.get_id():
            register.set_balance(register.get_balance()+int(amount))
            save_philbank()
            return
    new_register = Register(user_id, amount)
    philbank.append(new_register)
    save_philbank()


def get_philcoin_balance(user_id):
    for register in philbank:
        if user_id == register.get_id():
            return register.get_balance()
    return -1


def get_name_from_users(user_id):
    for user in client.users:
        if user.id == user_id:
            return user.name
    return None


def save_philbank():
    with open('philbank.txt', 'w') as f:
        for register in philbank:
            f.write("{'Name': '" + get_name_from_users(register.get_id()) + "','UserId': " + str(register.get_id())
                    + ",'Balance': " + str(register.get_balance()) + "}\n")


@client.event
async def on_reaction_add(reaction, user):
    if str(reaction).index("philcoin") >= 0:
        if reaction.message.author.id != user.id:
            add_philcoin(reaction.message.author.id, 1)


@client.event
async def on_ready():
    print('Phil Bot running')

    if not os.path.exists('philbank.txt'):
        open('philbank.txt', 'w')

    with open("philbank.txt", "r") as f:
        for line in f:
            new_register = eval(line)
            philbank.append(Register(new_register.get('UserId'), new_register.get('Balance')))

client.run(TOKEN)