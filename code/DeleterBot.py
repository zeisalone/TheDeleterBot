import discord
from discord.ext import commands
import json
import os

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

BANWORDS_FILE = 'banwords/banwords.json'

def load_banwords():
    if os.path.exists(BANWORDS_FILE):
        try:
            with open(BANWORDS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_banwords(words):
    with open(BANWORDS_FILE, 'w') as f:
        json.dump(words, f)

additional_bloat_words = load_banwords()
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

@tree.command(name="banword", description="Adds a word to the list of messages to be deleted.")
async def banword(interaction: discord.Interaction, word: str):
    lower_word = word.lower()
    if lower_word in additional_bloat_words:
        await interaction.response.send_message(f"ERROR: '{word}' is already in the banned list.", ephemeral=True)
    elif len(additional_bloat_words) >= 50:
        await interaction.response.send_message("ERROR: Cannot add more than 50 words to the banned list.", ephemeral=True)
    else:
        additional_bloat_words.append(lower_word)
        save_banwords(additional_bloat_words)
        await interaction.response.send_message(f"Added '{word}' to the banned list.", ephemeral=True)

@tree.command(name="showbanlist", description="Shows the words that have been banned.")
async def showbanlist(interaction: discord.Interaction):
    if not additional_bloat_words:
        embed = discord.Embed(title="Banned Words", description="No banned words.", color=discord.Color.red())
    else:
        words = "\n".join(additional_bloat_words[:50])
        embed = discord.Embed(
            title="Banned Words",
            description=f"**{len(additional_bloat_words)}/50**\n\n{words}",
            color=discord.Color.red()
        )

    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="helpdeleter", description="Shows this help message.")
async def helpdeleter(interaction: discord.Interaction):
    help_message = (
        "**DeleterBot Commands**\n"
        f"```/delmudaebloat - Enables/disables the deletion of spam messages from Mudae.\n"
        f"/delkarutabloat - Enables/disables the deletion of 'K!D' commands from users.\n"
        f"/deleteexpired - Deletes all expired messages from Karuta.\n"
        f"/banword <word> - Adds a word to the list of messages to be deleted.\n"
        f"/showbanlist - Shows the list of banned words.\n"
        f"/helpdeleter - Shows this help message.```"
    )
    await interaction.response.send_message(help_message, ephemeral=True)

@client.event
async def on_message(message):
    global delete_mudae_bloat, delete_karuta_bloat, additional_bloat_words

    if message.author == client.user:
        return
    lower_content = message.content.lower()
    if delete_mudae_bloat:
        if (lower_content.startswith('$') or any(word in lower_content for word in additional_bloat_words)) and message.author.name != MUDAE_BOT_NAME:
            await message.delete()
    if delete_karuta_bloat:
        if lower_content.startswith('k!d') and message.author.name != KARUTA_BOT_NAME:
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