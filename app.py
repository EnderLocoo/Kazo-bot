import discord
import os
from dotenv import load_dotenv
from bot import KazoBot, setup_slash_commands

load_dotenv()

TOKEN_BOT = os.getenv("TOKEN")
AUTO_ROLE_ID = 1392547680030560309
servidores_permitidos = [975245393090723903, 823835602138169374]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = KazoBot(command_prefix="%", intents=intents, auto_role_id=AUTO_ROLE_ID, servidores_permitidos=servidores_permitidos)
setup_slash_commands(bot)

bot.run(TOKEN_BOT)