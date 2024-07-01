import discord

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
client = discord.Client(intents=intents)

MUDAE_BOT_NAME = 'Mudae'
DELETE_COMMAND = '/delmudaebloat'

delete_mudae_bloat = False

@client.event
async def on_message(message):
    global delete_mudae_bloat

    if message.author == client.user:
        return
    if message.content.startswith(DELETE_COMMAND):
        delete_mudae_bloat = not delete_mudae_bloat
        status = "enabled" if delete_mudae_bloat else "disabled"
        await message.channel.send(f"Mudae bloat deletion {status}")
        if delete_mudae_bloat:
            await delete_existing_mudae_messages(message.channel)
        return
    if delete_mudae_bloat:
        if message.content.startswith('$') and message.author.name != MUDAE_BOT_NAME:
            await message.delete()

async def delete_existing_mudae_messages(channel):
    async for msg in channel.history(limit=None):
        if msg.content.startswith('$') and msg.author.name != MUDAE_BOT_NAME:
            await msg.delete()


client.run('placeholder')