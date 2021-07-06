from pathlib import Path

import discord
from discord.ext import commands


class Musicbot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(
            command_prefix=self.prefix,
            case_insensitive=True,
            intents=discord.Intents.all()
        ) # case_insensitive=True means play and Play are the same thing

    def setup(self):
        print("Setup Running...")
        
        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f"Loaded `{cog}` cog.")
        
        print("Setup Completed.")
    
    def run(self):
        self.setup()

        with open("data/token.0", "r", encoding="utf-8") as f:
            TOKEN = f.read()

        print("Running Bot...")
        super().run(TOKEN, reconnect=True)
    
    async def shutdown(slef):
        print("Closing connection To Discord...")
        await super().close()

    async def close(self):
        print("Closing On Keyboard Interrupt...")
        await super().shutdown()
    
    async def on_connect(self):
        print(f"Connect to Discord (latency: {self.latency*1000} ms.")

    async def on_resume(self):
        print("Bot Resumed.")
    
    async def on_disconnect(self):
        print("Bot Disconnected.")

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot Ready.")
    
    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("+")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None: 
           await self.invoke(ctx) 
    
    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)
