import discord
from discord import app_commands
import aiohttp
import random
import os
from flask import Flask
from threading import Thread

# Setup environment variables
TOKEN = os.getenv("TOKEN")
TENOR_API_KEY = os.getenv("TENOR_API_KEY")

# Setup Flask web server to respond to UptimeRobot ping
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# Start Flask web server in a separate thread
def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

# Setup Discord bot
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

# Command for horse GIF
@client.tree.command(name="horse", description="Sends a random horse GIF 🐴")
async def horse(interaction: discord.Interaction):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://tenor.googleapis.com/v2/search?q=horse&key={TENOR_API_KEY}&limit=20") as response:
            if response.status != 200:
                await interaction.response.send_message("Failed to fetch a horse GIF.", ephemeral=True)
                return
            data = await response.json()
            results = data.get("results", [])
            if not results:
                await interaction.response.send_message("No GIFs found!", ephemeral=True)
                return
            gif_url = random.choice(results)["media_formats"]["gif"]["url"]
            await interaction.response.send_message(gif_url)

# Run the Flask server in the background
keep_alive()

# Start the Discord bot
client.run(TOKEN)
