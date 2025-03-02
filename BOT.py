import asyncio
import sys
import requests
import discord
from discord.ext import commands

# ✅ Fix for Windows aiodns issue
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TOKEN = "MTM0NTM3Nzg1NDI3NTQ1NzA1Ng.Ghswfv.FoACcSakBxWqU6DXDvke3fFkCtq4yMypABAOVI"
CHANNEL_ID = 1345839597921374288  # Replace with your Discord channel ID

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # ✅ Important for reading messages

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    """Auto-respond when someone types !checkban <uid> in the specific channel."""
    if message.author == bot.user:
        return  # Ignore bot's own messages

    if message.channel.id == CHANNEL_ID and message.content.startswith("!checkban "):
        uid = message.content.split(" ")[1]  # Extract UID from message
        await checkban(message.channel, uid)

async def checkban(channel, uid):
    """Check if a Free Fire account is banned using Paul Alfredo's API"""
    url = f"https://api.paulalfredo.me/check_ban/{uid}"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")  # Debugging

        if response.status_code == 200:
            data = response.json()
            print(f"🔍 API Response: {data}")  # Debugging

            # Extracting data correctly
            if "data" in data and "is_banned" in data["data"]:
                is_banned = data["data"]["is_banned"]
                period = data["data"].get("period", "Unknown")  # Ban period if available

                if is_banned == 1:  # If is_banned = 1, user is banned
                    msg = f"**ID {uid} IS BANED!**\nUNBAN DATE: **AFTER {period} DAYS**"
                    gif_url = "https://media.discordapp.net/attachments/1345377699090399292/1345782653932146778/standard.gif?ex=67c5cd44&is=67c47bc4&hm=ed5822b2a2f9e5db4f49aeb38e1e370a187ba9e0399c7073cc651569b7cf03d0&="
                else:
                    msg = f"**ID {uid} IS NOT BANED!**"
                    gif_url = "https://media.discordapp.net/attachments/1345377699090399292/1345782488466722876/standard_1.gif?ex=67c5cd1c&is=67c47b9c&hm=7b0acc9ae7b3c7dea3f7eace2a35fe5636e80d7c7471939fdad1d9edc69e42a6&="

                await channel.send(msg)
                await channel.send(gif_url)  # Send GIF

            else:
                msg = f"API Response Unexpected Format: {data}"  # If "data" key is missing
                await channel.send(msg)

        elif response.status_code == 404:
            msg = f"UID {uid} NOT FOUND"
            await channel.send(msg)
        else:
            msg = f"API Error Contect With Fusion: {response.status_code}"
            await channel.send(msg)

    except requests.exceptions.RequestException as e:
        msg = f"Error Contect With Fusion : {e}"
        await channel.send(msg)

bot.run(TOKEN)
