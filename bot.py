import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class KazoBot(commands.Bot):
    def __init__(self, command_prefix, intents, auto_role_id, servidores_permitidos):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.auto_role_id = auto_role_id
        self.servidores_permitidos = servidores_permitidos

    async def setup_hook(self):
        await self.tree.sync()

    async def on_guild_join(self, guild):
        if guild.id not in self.servidores_permitidos:
            print(f"El bot fue añadido a un servidor no autorizado: {guild.name} (ID: {guild.id}). Abandonando...")
            await guild.leave()

    async def on_ready(self):
        print(f"✅ El bot está en línea como {self.user}")

    async def on_member_join(self, member):
        if member.bot:
            print(f"🤖 Ignorando bot: {member.name}")
            return

        print(f"📥 Nuevo miembro: {member.name}")

        role = member.guild.get_role(self.auto_role_id)
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

# Slash commands
def setup_slash_commands(bot: KazoBot):
    @bot.tree.command(name="ayuda", description="Muestra el mensaje de ayuda")
    async def ayuda(interaction: discord.Interaction):
        usuario = interaction.user.name
        help_text = (
            f"Hola {usuario}! Soy Kazo-Bot. Aquí tienes algunos comandos que puedes usar:\n"
            "- `/ayuda`: Muestra este mensaje de ayuda.\n"
            "- `/info`: Información sobre el bot.\n"
            "- `/redes`: Enlaces a las redes sociales de Kazo.\n"
            "¡Disfruta del servidor!"
        )
        await interaction.response.send_message(help_text)

    @bot.tree.command(name="info", description="Información sobre el bot")
    async def info(interaction: discord.Interaction):
        embed = discord.Embed(
            title="Información del Bot",
            description="Un bot para gestionar a los nuevos miembros del servidor, asignando un rol temporalmente.",
            color=discord.Color.purple()
        )
        embed.add_field(name="Nombre", value="Kazo-Bot", inline=True)
        embed.add_field(name="Versión", value="1.0", inline=True)
        embed.add_field(name="Desarrollador", value="Darking", inline=True)
        embed.add_field(name="Comandos disponibles", value="`/ayuda`, `/info`, `/redes`", inline=False)
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="redes", description="Redes sociales de Kazo Sensei")
    async def redes(interaction: discord.Interaction):
        embed = discord.Embed(
            title="Redes Sociales de Kazo Sensei",
            description="Un link directo a las redes de Kazo Sensei.",
            color=discord.Color.purple()
        )
        embed.add_field(name="<:twitch_icon:1393663624072925224> Twitch", value="[KazoSensei_](https://www.twitch.tv/kazosensei_)", inline=True) # Twitch
        embed.add_field(name="<:youtube_icon:1393666522660077630> YouTube", value="[Kazo Sensei](https://www.youtube.com/@kazosensei)\n[Futuro Gamer](https://www.youtube.com/@FuturoGamer-)", inline=True) # YouTube
        embed.add_field(name="<:tiktok_icon:1393739688178876499> TikTok", value="[KazoSensei](https://www.tiktok.com/@kazosensei_)\n[futurogamer_](https://www.tiktok.com/@futurogamer_)", inline=True) # TikTok
        embed.add_field(name="<:instagram_icon:1393743761976332318> Instagram", value="[kazosensei_](https://www.instagram.com/kazosensei_/)\n[futurogameroficial](https://www.instagram.com/futurogameroficial/)", inline=True) # Instagram
        embed.add_field(name="<:threads_icon:1393744739681046681> Threads", value="[Kazo](https://www.threads.com/@kazosensei_)", inline=True) # Threads
        embed.add_field(name="<:twitter_icon:1393746897881006100> Twitter (X)", value="[Kazo Sensei](https://x.com/KazoSensei_)", inline=True)

        await interaction.response.send_message(embed=embed)