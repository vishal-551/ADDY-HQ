from __future__ import annotations

import discord
from discord.ext import commands

from bot.core.guild_bootstrap import bootstrap_guild
from bot.core.healthcheck import in_memory_health
from shared.logger import get_logger

log = get_logger("bot.events")


class CoreEvents(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        log.info("ready", user=str(self.bot.user), guilds=len(self.bot.guilds), health=in_memory_health())

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        await bootstrap_guild(self.bot, guild)
        log.info("guild_joined", guild_id=guild.id, guild_name=guild.name)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CoreEvents(bot))
