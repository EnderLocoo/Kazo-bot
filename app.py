import discord
from discord.ext import commands
import asyncio  # Para usar sleep (espera de tiempo)
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Asignamos las variables de entorno
TOKEN_BOT = os.getenv("TOKEN")
AUTO_ROLE_ID = 1392547680030560309  # Reemplaza este número por el ID de tu rol

# Intents son necesarios para poder detectar eventos como "nuevo miembro"
intents = discord.Intents.default()
intents.members = True  # Activamos la detección de nuevos miembros
intents.message_content = True  # Activamos la detección de contenido de mensajes

# Creamos el bot con prefijo y los intents activados
bot = commands.Bot(command_prefix="%", intents=intents)

# Evento: cuando el bot esté listo para funcionar
@bot.event
async def on_ready():
    print(f"✅ El bot está en línea como {bot.user}")

# Evento: cuando un nuevo miembro entra al servidor
@bot.event
async def on_member_join(member):
    if member.bot:
        print(f"🤖 Ignorando bot: {member.name}")
        return  # Ignoramos los bots

    print(f"📥 Nuevo miembro: {member.name}")

    role = member.guild.get_role(AUTO_ROLE_ID)
    if role is None:
        print("❌ Rol no encontrado. Verifica el ID del rol.")
        return

    try:
        await member.add_roles(role)
        print(f"✅ Rol '{role.name}' asignado a {member.name}")
        await asyncio.sleep(1 * 60 * 60)
        if role in member.roles:
            await member.remove_roles(role)
            print(f"⏳ 4 horas pasaron. Rol removido de {member.name}")

    except discord.Forbidden:
        print("🚫 No tengo permisos para gestionar roles.")
    except Exception as e:
        print(f"⚠️ Ocurrió un error: {e}")

@bot.command(name="ayuda")
async def help_command(ctx):
    usuario = ctx.author.name
    help_text = (
        f"Hola {usuario}! Soy Kazo-Bot. Aquí tienes algunos comandos que puedes usar:\n"
        "- `%ayuda`: Muestra este mensaje de ayuda.\n"
        "- `%info`: Información sobre el bot.\n"
        "¡Disfruta del servidor!"
    )
    await ctx.reply(help_text, mention_author=False)

@bot.command(name="info")
async def info_command(ctx):
    info_text = (
        "## **Información del Bot:**\n"
        "- **Nombre:** Kazo-Bot\n"
        "- **Versión:** 1.0\n"
        "- **Desarrollador:** Darking\n"
        "- **Descripción:** Un bot para gestionar a los nuevos miembros del servidor, asignando un rol temporalmente.\n"
        "\n"
        "- **Comandos disponibles:**\n"
        "  - `%ayuda`: Muestra la lista de comandos.\n"
        "  - `%info`: Muestra esta información."
    )
    await ctx.reply(info_text, mention_author=False)


# Reemplaza esto con tu token real
bot.run(TOKEN_BOT)