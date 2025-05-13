{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import discord\
from discord import app_commands\
import aiohttp\
import random\
import os\
\
from flask import Flask\
from threading import Thread\
from dotenv import load_dotenv\
\
# Load environment variables\
load_dotenv()\
TOKEN = os.getenv("TOKEN")\
TENOR_API_KEY = os.getenv("TENOR_API_KEY")\
\
# Web server to keep alive\
app = Flask('')\
@app.route('/')\
def home():\
    return "I'm alive!"\
def run():\
    app.run(host='0.0.0.0', port=8080)\
def keep_alive():\
    Thread(target=run).start()\
\
# Discord client\
class MyClient(discord.Client):\
    def __init__(self):\
        intents = discord.Intents.default()\
        super().__init__(intents=intents)\
        self.tree = app_commands.CommandTree(self)\
\
    async def setup_hook(self):\
        await self.tree.sync()\
\
client = MyClient()\
\
@client.event\
async def on_ready():\
    print(f'Logged in as \{client.user\}!')\
\
@client.tree.command(name="horse", description="Send a random horse GIF \uc0\u55357 \u56372 ")\
async def horse(interaction: discord.Interaction):\
    async with aiohttp.ClientSession() as session:\
        async with session.get(\
            f"https://tenor.googleapis.com/v2/search?q=horse&key=\{TENOR_API_KEY\}&limit=20"\
        ) as response:\
            if response.status != 200:\
                await interaction.response.send_message("Failed to fetch GIF.", ephemeral=True)\
                return\
\
            data = await response.json()\
            results = data.get("results", [])\
            if not results:\
                await interaction.response.send_message("No GIFs found!", ephemeral=True)\
                return\
\
            gif_url = random.choice(results)["media_formats"]["gif"]["url"]\
            await interaction.response.send_message(gif_url)\
\
keep_alive()\
client.run(TOKEN)\
}