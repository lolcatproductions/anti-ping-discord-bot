import logging
import dotenv, os
import discord
import json

logging.basicConfig(level=logging.INFO)


## load files
dotenv.load_dotenv()
TOKEN = str(os.getenv("TOKEN"))

with open("config.json", "r") as f:
    config = json.load(f)

print("config content:", config)


## start bot
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)


## bot code
@bot.event
async def on_ready():
    print("logged in as", bot.user)


@bot.event
async def on_message(message: discord.Message):
    if message.author.id == bot.user.id:  # Make sure we won't be replying to ourselves.
        return
    
    if len(message.mentions) == 0:  # check if message pings anyone; if not, stop
        return
    
    for member in message.mentions:
        if discord.Guild.get_role(message.guild, config["no-pings-role-id"]) in member.roles:  # check if member has the [no pings] role
            if message.type == discord.MessageType.reply:  # check if the message is a reply
                reply = config["replies"]["ping_reply"]
            else:
                reply = config["replies"]["ping_no_reply"]
    
            await message.reply(reply)
            break  # to prevent the bot from sending the warning multiple times

if __name__ == "__main__":
    bot.run(TOKEN)