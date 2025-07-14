import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv(".env.imagenes")

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
                print(f"⏳ 1 hora pasó. Rol removido de {member.name}")
                try:
                    embed = discord.Embed(
                        title="Acceso limitado removido",
                        description=f"Buenas {member.name}! Te informo de que se te ha retirado el rol temporal asignado al unirte al servidor. Ya puedes interactuar con el servidor sin restricciones.\nSi tienes dudas, contacta a un moderador.\n\n-# PD: Este es un mensaje automático, no respondas a este mensaje.",
                        color=discord.Color.purple()

                    )

                    embed.set_thumbnail(url=f"{os.getenv('IMAGEN_KAZO')}")  # URL de la imagen del thumbnail

                    embed.set_footer(
                        text="La familia de Kazo",
                        icon_url=f"{os.getenv('IMAGEN_KAZO')}"  # Texto e icono del pie de página
                    )

                    await member.send(
                        f"¡Buenas {member.name}! Te informo de que se te ha retirado el rol temporal asignado al unirte al servidor. Ya puedes interactuar con el servidor sin restricciones.\n\n"
                        "Si tienes dudas, contacta a un moderador."
                        "\n\nPD: Este es un mensaje automático, no respondas a este mensaje."
                        "\n-# La familia de Kazo"
                    )
                    print(f"📩 Mensaje privado enviado a {member.name}")
                except Exception as dm_error:
                    print(f"⚠️ No se pudo enviar mensaje privado a {member.name}: {dm_error}")

        except discord.Forbidden:
            print("🚫 No tengo permisos para gestionar roles.")
        except Exception as e:
            print(f"⚠️ Ocurrió un error: {e}")

# Slash commands
def setup_slash_commands(bot: KazoBot):
    @bot.tree.command(name="info", description="Muestra información sobre el bot")
    async def info(interaction: discord.Interaction):
        embed = discord.Embed(
            title="📘 | Información del Bot",
            description="Un bot destinado a ayudar a la comunidad de Kazo Sensei. Se irán añadiendo más funcionalidades con el tiempo.",
            color=discord.Color.purple()
        )
        embed.add_field(name="Nombre", value="Kazo-Bot", inline=True)
        embed.add_field(name="Versión", value=f"{os.getenv('VERSION')}", inline=True)
        embed.add_field(name="Desarrollador", value="Darking", inline=True)
        embed.add_field(name="Comandos disponibles", value="`/info`, `/redes`", inline=False)

        embed.set_thumbnail(url=f"{os.getenv('IMAGEN_REDES')}") # URL de la imagen del thumbnail

        embed.set_footer(
            text="La familia de Kazo",
            icon_url=f"{os.getenv('IMAGEN_KAZO')}") # Texto e icono del pie de página
        
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="redes", description="Muestra las redes sociales de Kazo Sensei")
    async def redes(interaction: discord.Interaction):
        embed = discord.Embed(
            title="👥 | Redes Sociales de Kazo Sensei",
            color=discord.Color.purple()
        )
        embed.add_field(name="<:twitch_icon:1393663624072925224> Twitch", value="[KazoSensei_](https://www.twitch.tv/kazosensei_)", inline=True) # Twitch
        embed.add_field(name="<:youtube_icon:1393666522660077630> YouTube", value="[Kazo Sensei](https://www.youtube.com/@kazosensei)\n[Futuro Gamer](https://www.youtube.com/@FuturoGamer-)", inline=True) # YouTube
        embed.add_field(name="<:tiktok_icon:1393739688178876499> TikTok", value="[KazoSensei](https://www.tiktok.com/@kazosensei_)\n[futurogamer_](https://www.tiktok.com/@futurogamer_)", inline=True) # TikTok
        embed.add_field(name="<:instagram_icon:1393743761976332318> Instagram", value="[kazosensei_](https://www.instagram.com/kazosensei_/)\n[futurogameroficial](https://www.instagram.com/futurogameroficial/)", inline=True) # Instagram
        embed.add_field(name="<:threads_icon:1393744739681046681> Threads", value="[Kazo](https://www.threads.com/@kazosensei_)", inline=True) # Threads
        embed.add_field(name="<:twitter_icon:1393746897881006100> Twitter (X)", value="[Kazo Sensei](https://x.com/KazoSensei_)", inline=True)

        embed.set_thumbnail(url=f"{os.getenv('IMAGEN_REDES')}") # Imagen del thumbnail
        
        embed.set_footer(
            text="La familia de Kazo",
            icon_url=f"{os.getenv('IMAGEN_KAZO')}") # Texto e icono del pie de página

        await interaction.response.send_message(embed=embed)