import discord
import os
from dotenv import load_dotenv
from bot import KazoBot, setup_slash_commands

load_dotenv()

TOKEN_BOT = os.getenv("TOKEN")
AUTO_ROLE_ID = int(os.getenv("AUTO_ROLE_ID"))
servidores_permitidos = [int(sid) for sid in os.getenv("SERVIDORES_PERMITIDOS").split(",")]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = KazoBot(command_prefix="%", intents=intents, auto_role_id=AUTO_ROLE_ID, servidores_permitidos=servidores_permitidos)
setup_slash_commands(bot)

bot.run(TOKEN_BOT)