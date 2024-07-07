import discord

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
client = discord.Client(intents=intents)

MUDAE_BOT_NAME = 'Mudae'
KARUTA_BOT_NAME = 'Karuta'
DELETE_MUDAE_COMMAND = '/delmudaebloat'
DELETE_KARUTA_COMMAND = '/delkarutabloat'
DELETE_EXPIRED_COMMAND = '/deleteexpired'
ADD_BLOAT_COMMAND = ''
HELP_COMMAND = '/helpdeleter'
delete_mudae_bloat = False
delete_karuta_bloat = False
additional_bloat_words = []
@client.event
async def on_message(message):
    global delete_mudae_bloat, delete_karuta_bloat, additional_bloat_words

    if message.author == client.user:
        return
    if message.content.startswith(DELETE_MUDAE_COMMAND):
        delete_mudae_bloat = not delete_mudae_bloat
        status = "enabled" if delete_mudae_bloat else "disabled"
        await message.channel.send(f"Mudae bloat deletion {status}")
        if delete_mudae_bloat:
            await delete_existing_mudae_messages(message.channel)
        return
    if message.content.startswith(DELETE_KARUTA_COMMAND):
        delete_karuta_bloat = not delete_karuta_bloat
        status = "enabled" if delete_karuta_bloat else "disabled"
        await message.channel.send(f"Karuta bloat deletion {status}")
        if delete_karuta_bloat:
            await delete_existing_karuta_messages(message.channel)
        return
    if message.content.startswith(DELETE_EXPIRED_COMMAND):
        await delete_expired_karuta_messages(message.channel)
        return
    if message.content.startswith(ADD_BLOAT_COMMAND):
        new_bloat_word = message.content[len(ADD_BLOAT_COMMAND):].strip()
        if new_bloat_word:
            additional_bloat_words.append(new_bloat_word)
            await message.channel.send(f"Added '{new_bloat_word}' to the bloat list.")
        else:
            await message.channel.send("Please provide a word to add.")
        return
    if message.content.startswith(HELP_COMMAND):
        help_message = (
            "**DeleterBot Commands**\n"
            f"```{DELETE_MUDAE_COMMAND} - Enables/disables the deletion of spam messages from Mudae.\n"
            f"{DELETE_KARUTA_COMMAND} - Enables/disables the deletion of 'K!D' commands from users.\n"
            f"{DELETE_EXPIRED_COMMAND} - Deletes all expired messages from Karuta.\n"
            f"{ADD_BLOAT_COMMAND} <word> - Adds a word to the list of messages to be deleted.```"
        )
        await message.channel.send(help_message)
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
        async for msg in after.channel.history(limit=100):  # Limite para evitar busca intensa
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