import aiohttp
import discord
import io
import config

from ImageHandler import juan_processing
from Philbank import start_bank, add_philcoin, get_philcoin_balance

BOT_PREFIX = ("!")
TOKEN = config.token

client = discord.Client()


def get_name_from_user_id(user_id):
    for user in client.users:
        if user.id == user_id:
            return user.name
    return None


def process_command(command):
    if command.author.id == client.user.id:
        return False
    try:
        if command.content.index(BOT_PREFIX) == 0:
            return command.content[1:].split()
        else:
            return False
    except ValueError:
        return False
    print(f'Weird command failure: {command.content}')
    return False


@client.event
async def on_message(message):
    command = process_command(message)

    if not command:
        return

    if command[0] == "philbalance":
        await message.author.send(
            f"User: {get_name_from_user_id(message.author.id)}, Balance: {get_philcoin_balance(message.author.id)}")
    elif command[0] == "juan":
        async with aiohttp.ClientSession() as session:
            async with session.get(command[1]) as resp:
                buffer = io.BytesIO(await resp.read())

        await message.channel.send(file=discord.File(fp=juan_processing(buffer), filename="image.png"))


@client.event
async def on_reaction_add(reaction, user):
    msg_author = reaction.message.author
    if str(reaction).index("philcoin") >= 0:
        if msg_author.id != user.id:
            add_philcoin(msg_author.id, get_name_from_user_id(msg_author.id), 1)


@client.event
async def on_ready():
    print('Phil Bot running')
    print(start_bank())

client.run(TOKEN)
