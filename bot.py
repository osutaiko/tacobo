import discord
import responses
from beatmap import *
import re
from image_creation import *


async def send_message(message, user_message):
    try:
        response = responses.get_response(user_message)
        await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = '*****************' #Issue your own token from Discord
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username}: "{user_message}" ({channel})')

        if user_message[0] == '+':
            user_message = user_message[1:]
            await send_message(message, user_message)

            if user_message[:5] == 'image':
                command = user_message.lower().split()
                mapset_id = int(re.search(r'sets/(.*?)#', command[1]).group(1))
                map_id = int(user_message.strip().split('/')[-1])
                download_mapset(mapset_id)
                find_diff_name(map_id)
                await message.channel.send("Requested image:", file=discord.File(map_to_image(parse_map(map_id))))


    client.run(TOKEN)