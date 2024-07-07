import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
client = commands.Bot(command_prefix="/", intents=intents)
tree = client.tree
MUDAE_BOT_NAME = 'Mudae'
KARUTA_BOT_NAME = 'Karuta'
delete_mudae_bloat = False
delete_karuta_bloat = False
additional_bloat_words = []

@tree.command(name="delmudaebloat", description="Enables/disables the deletion of spam messages from Mudae.")
async def delmudaebloat(interaction: discord.Interaction):
    global delete_mudae_bloat
    delete_mudae_bloat = not delete_mudae_bloat
    status = "enabled" if delete_mudae_bloat else "disabled"
    await interaction.response.send_message(f"Mudae bloat deletion {status}", ephemeral=True)
    if delete_mudae_bloat:
        await delete_existing_mudae_messages(interaction.channel)

@tree.command(name="delkarutabloat", description="Enables/disables the deletion of 'K!D' commands from users.")
async def delkarutabloat(interaction: discord.Interaction):
    global delete_karuta_bloat
    delete_karuta_bloat = not delete_karuta_bloat
    status = "enabled" if delete_karuta_bloat else "disabled"
    await interaction.response.send_message(f"Karuta bloat deletion {status}", ephemeral=True)
    if delete_karuta_bloat:
        await delete_existing_karuta_messages(interaction.channel)

@tree.command(name="deleteexpired", description="Deletes all expired messages from Karuta.")
async def deleteexpired(interaction: discord.Interaction):
    await delete_expired_karuta_messages(interaction.channel)
    await interaction.response.send_message("Deleted all expired messages from Karuta.", ephemeral=True)

@tree.command(name="addbloat", description="Adds a word to the list of messages to be deleted.")
async def addbloat(interaction: discord.Interaction, word: str):
    additional_bloat_words.append(word)
    await interaction.response.send_message(f"Added '{word}' to the bloat list.", ephemeral=True)

@tree.command(name="helpdeleter", description="Shows this help message.")
async def helpdeleter(interaction: discord.Interaction):
    help_message = (
        "**DeleterBot Commands**\n"
        f"```/delmudaebloat - Enables/disables the deletion of spam messages from Mudae.\n"
        f"/delkarutabloat - Enables/disables the deletion of 'K!D' commands from users.\n"
        f"/deleteexpired - Deletes all expired messages from Karuta.\n"
        f"/addbloat <word> - Adds a word to the list of messages to be deleted.\n"
        f"/helpdeleter - Shows this help message.```"
    )
    await interaction.response.send_message(help_message, ephemeral=True)

@client.event
async def on_message(message):
    global delete_mudae_bloat, delete_karuta_bloat, additional_bloat_words

    if message.author == client.user:
        return

    if delete_mudae_bloat:
        if (message.content.startswith('$') or any(word in message.content for word in additional_bloat_words)) and message.author.name != MUDAE_BOT_NAME:
            await message.delete()

    if delete_karuta_bloat:
        if message.content.lower().startswith('k!d') and message.author.name != KARUTA_BOT_NAME:
            await message.delete()

@client.event
async def on_message_edit(before, after):
    if "this drop has expired and the cards can no longer be grabbed." in after.content.lower():
        async for msg in after.channel.history(limit=100):
            if msg.author.name == KARUTA_BOT_NAME and msg.content.lower().startswith('k!d'):
                await msg.delete()
                break

async def delete_existing_mudae_messages(channel):
    async for msg in channel.history(limit=None):
        if msg.content.startswith('$') and msg.author.name != MUDAE_BOT_NAME:
            await msg.delete()

async def delete_existing_karuta_messages(channel):
    async for msg in channel.history(limit=None):
        if msg.content.lower().startswith('k!d') and msg.author.name != KARUTA_BOT_NAME:
            await msg.delete()

async def delete_expired_karuta_messages(channel):
    async for msg in channel.history(limit=None):
        if "this drop has expired and the cards can no longer be grabbed." in msg.content.lower():
            await msg.delete()

client.run('placeholder')