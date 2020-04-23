import io
import aiohttp
import discord
from Philbank import start_bank, add_philcoin, get_philcoin_balance

from PIL import Image

BOT_PREFIX = ("!")
TOKEN = ''

client = discord.Client()

COORDS = [(631, 551), (990, 550), (634, 308), (980, 339)]
COEFFS = [0.6547747129877984, 0.008083638431858402, -1670.4677146851654, -0.05607509889913542,
          0.6258704586809742, -628.8659542867306, -7.95610829238863e-05, 4.137514033619954e-05]


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


def process_image(buffer):
    width, height = 1219, 684
    im = Image.open(buffer).convert(mode='RGBA')
    im = im.resize((width, height), resample=Image.ANTIALIAS)
    bg = Image.open('data/img/juan_bg.png').convert(mode='RGBA')
    im = im.transform((width * 4, height * 4), Image.PERSPECTIVE, COEFFS, Image.BICUBIC)
    im = im.resize((bg.width, bg.height), resample=Image.ANTIALIAS)

    bg = Image.alpha_composite(bg, im)

    fg = Image.open('data/img/juan_fg.png').convert(mode='RGBA')
    bg = Image.alpha_composite(bg, fg)

    output = io.BytesIO()
    bg.save(output, format='png')
    output.seek(0)
    return output


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

        await message.channel.send(file=discord.File(fp=process_image(buffer), filename="image.png"))


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
