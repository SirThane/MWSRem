# -*- coding: utf-8 -*-

# Lib
from contextlib import suppress
from os import popen
from os.path import exists, join
from pickle import dump
from copy import deepcopy
# Site
# from discord.abc import Messageable
# from discord.channel import TextChannel
from discord import AppInfo, Permissions
from discord.embeds import Embed
from discord.ext.commands.cog import Cog
from discord.ext.commands.context import Context
from discord.ext.commands.core import command, group, is_owner
from discord.ext.commands.errors import (
    # BadArgument,
    ExtensionAlreadyLoaded,
    ExtensionFailed,
    ExtensionNotFound,
    ExtensionNotLoaded,
    NoEntryPointError
)

# Local

from utils.classes import Bot  # , GlobalTextChannelConverter


class Admin(Cog):
    """Administrative Commands"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.say_dest = None

    """ ######################
         Managing Bot Modules
        ###################### """

    @is_owner()
    @group(name="module", aliases=["cog", "mod"], invoke_without_command=True)
    async def module(self, ctx: Context):
        """Base command for managing bot modules

        Use without subcommand to list currently loaded modules"""

        modules = {module.__module__: cog for cog, module in self.bot.cogs.items()}
        space = len(max(modules.keys(), key=len))

        fmt = "\n".join([f"{module}{' ' * (space - len(module))} : {cog}" for module, cog in modules.items()])

        em = Embed(
            title="Administration: Currently Loaded Modules",
            description=f"```py\n{fmt}\n```",
            color=0x00FF00
        )
        await ctx.send(embed=em)

    @is_owner()
    @module.command(name="load", usage="(module name)")
    async def load(self, ctx: Context, module: str):
        """load a module

        If `verbose=True` is included at the end, error tracebacks will
        be sent to the errorlog channel"""

        module = f"cogs.{module}"

        try:
            self.bot.load_extension(module)

        except ExtensionNotFound:
            em = Embed(
                title="Administration: Load Module Failed",
                description=f"**__ExtensionNotFound__**\n"
                            f"No module `{module}` found in cogs directory",
                color=0xFF0000
            )

        except ExtensionAlreadyLoaded:
            em = Embed(
                title="Administration: Load Module Failed",
                description=f"**__ExtensionAlreadyLoaded__**\n"
                            f"Module `{module}` is already loaded",
                color=0xFF0000
            )

        except NoEntryPointError:
            em = Embed(
                title="Administration: Load Module Failed",
                description=f"**__NoEntryPointError__**\n"
                            f"Module `{module}` does not define a `setup` function",
                color=0xFF0000
            )

        except ExtensionFailed as error:
            if isinstance(error.original, TypeError):
                em = Embed(
                    title="Administration: Load Module Failed",
                    description=f"**__ExtensionFailed__**\n"
                                f"The cog loaded by `{module}` must be a subclass of discord.ext.commands.Cog",
                    color=0xFF0000
                )
            else:
                em = Embed(
                    title="Administration: Load Module Failed",
                    description=f"**__ExtensionFailed__**\n"
                                f"An execution error occurred during module `{module}`'s setup function",
                    color=0xFF0000
                )

        except Exception as error:
            em = Embed(
                title="Administration: Load Module Failed",
                description=f"**__{type(error).__name__}__**\n"
                            f"```py\n"
                            f"{error}\n"
                            f"```",
                color=0xFF0000
            )

        else:
            em = Embed(
                title="Administration: Load Module",
                description=f"Module `{module}` loaded successfully",
                color=0x00FF00
            )

        await ctx.send(embed=em)

    @is_owner()
    @module.command(name="unload", usage="(module name)")
    async def unload(self, ctx: Context, module: str):
        """Unload a module

        If `verbose=True` is included at the end, error tracebacks will
        be sent to the errorlog channel"""

        module = f"cogs.{module}"

        try:
            self.bot.unload_extension(module)

        except ExtensionNotLoaded:
            em = Embed(
                title="Administration: Unload Module Failed",
                description=f"**__ExtensionNotLoaded__**\n"
                            f"Module `{module}` is not loaded",
                color=0xFF0000
            )

        except Exception as error:
            em = Embed(
                title="Administration: Unload Module Failed",
                description=f"**__{type(error).__name__}__**\n"
                            f"```py\n"
                            f"{error}\n"
                            f"```",
                color=0xFF0000
            )

        else:
            em = Embed(
                title="Administration: Unload Module",
                description=f"Module `{module}` unloaded successfully",
                color=0x00FF00
            )

        await ctx.send(embed=em)

    @is_owner()
    @module.command(name="reload", usage="(module name)")
    async def reload(self, ctx: Context, module: str):
        """Reload a module

        If `verbose=True` is included at the end, error tracebacks will
        be sent to the errorlog channel"""

        module = f"cogs.{module}"

        try:
            self.bot.reload_extension(module)

        except ExtensionNotLoaded:
            em = Embed(
                title="Administration: Reload Module Failed",
                description=f"**__ExtensionNotLoaded__**\n"
                            f"Module `{module}` is not loaded",
                color=0xFF0000
            )

        except ExtensionNotFound:
            em = Embed(
                title="Administration: Reload Module Failed",
                description=f"**__ExtensionNotFound__**\n"
                            f"No module `{module}` found in cogs directory",
                color=0xFF0000
            )

        except NoEntryPointError:
            em = Embed(
                title="Administration: Reload Module Failed",
                description=f"**__NoEntryPointError__**\n"
                            f"Module `{module}` does not define a `setup` function",
                color=0xFF0000
            )

        except ExtensionFailed as error:
            if isinstance(error.original, TypeError):
                em = Embed(
                    title="Administration: Reload Module Failed",
                    description=f"**__ExtensionFailed__**\n"
                                f"The cog loaded by `{module}` must be a subclass of discord.ext.commands.Cog",
                    color=0xFF0000
                )
            else:
                em = Embed(
                    title="Administration: Reload Module Failed",
                    description=f"**__ExtensionFailed__**\n"
                                f"An execution error occurred during module `{module}`'s setup function",
                    color=0xFF0000
                )

        except Exception as error:
            em = Embed(
                title="Administration: Reload Module Failed",
                description=f"**__{type(error).__name__}__**\n"
                            f"```py\n"
                            f"{error}\n"
                            f"```",
                color=0xFF0000
            )

        else:
            em = Embed(
                title="Administration: Reload Module",
                description=f"Module `{module}` reloaded successfully",
                color=0x00FF00
            )

        await ctx.send(embed=em)

    """ ######################
         General Use Commands
        ###################### """

    # @is_owner()
    # @group(name="say", invoke_without_command=True)
    # async def say(self, ctx: Context, *, msg: str = ""):
    #     """Makes the bot send a message
    #
    #     If self.say_dest is set, it will send the message there
    #     If it is not, it will send to ctx.channel"""
    #
    #     dest: Messageable = self.say_dest if self.say_dest else ctx.channel
    #     await dest.send(msg)
    #
    # @is_owner()
    # @say.command(name="in")
    # async def say_in(self, ctx: Context, dest: str = None):
    #     """Sets the destination for messages from `[p]say`"""
    #
    #     if dest:
    #         try:
    #             self.say_dest: TextChannel = await GlobalTextChannelConverter().convert(ctx, dest)
    #         except BadArgument as error:
    #             em = Embed(
    #                 title="Invalid Channel Identifier",
    #                 description=f"**__{type(error).__name__}__**: {str(error)}",
    #                 color=0xFF0000
    #             )
    #             await ctx.send(embed=em)
    #         else:
    #             em = Embed(
    #                 title="Administration: Set `say` Destination",
    #                 description=f"__Say destination set__\n"
    #                             f"Guild: {self.say_dest.guild.name}\n"
    #                             f"Channel: {self.say_dest.mention}\n"
    #                             f"ID: {self.say_dest.id}",
    #                 color=0x00FF00
    #             )
    #             await ctx.send(embed=em)
    #     else:
    #         self.say_dest = None
    #         em = Embed(
    #             title="Administration: Set `say` Destination",
    #             description=f"Say destination has been unset",
    #             color=0x00FF00
    #         )
    #         await ctx.send(embed=em)

    """ #########################
         Updating and Restarting
        ######################### """

    @staticmethod
    def gitpull() -> str:
        """Uses os.popen to `git pull`"""
        resp = popen("git pull").read()
        resp = f"```diff\n{resp}\n```"
        return resp

    @is_owner()
    @command(name="pull")
    async def pull(self, ctx: Context):
        """Updates bot repo from master"""

        em = Embed(
            title="Administration: Git Pull",
            description=self.gitpull(),
            color=0x00FF00
        )
        await ctx.send(embed=em)

    @is_owner()
    @group(name='restart', aliases=["kill", "f"], invoke_without_command=True)
    async def _restart(self, ctx: Context):
        """Restarts the bot"""

        em = Embed(
            title="Administration: Restart",
            description=f"{ctx.author.mention} initiated bot restart.",
            color=0x00FF00
        )
        for x_loop in self.bot.univ.Loops:
            x_loop.cancel()

        await ctx.send(embed=em)
        with suppress(RuntimeError, RuntimeWarning):
            await self.bot.logout()

    @is_owner()
    @command(name="config", aliases=["bot"])

    async def settings(self, ctx, option = None, new_value = None):

        """Manage Bot settings"""
        em = Embed(title="Administration: Config", description="Description not set.", color=0x000000)
        if option:
            if option == "auto_pull":
                if new_value in ["True", "False"]:
                    original = deepcopy(self.bot.auto_pull)
                    if new_value == "True":
                        self.bot.auto_pull = True
                    elif new_value == "False":
                        self.bot.auto_pull = False

                    em.description = f"{ctx.author.mention} updated \"{option}\" to \"{new_value}\".\n`Original value: {original}`"
                    em.color = 0x00FF00

                elif new_value:
                    em.description = f"An improper value was passed.\n`Valid responses for {option}: [True], [False]`"
                    em.color = 0xFF0000

                elif not new_value:
                    em.description = f"The current value for {option} is:\n`{self.bot.auto_pull}`"
                    em.color = 0x0000FF

            elif option == "debug_mode":
                if new_value in ["True", "False"]:
                    original = deepcopy(self.bot.debug_mode)
                    if new_value == "True":
                        self.bot.debug_mode = True
                    elif new_value == "False":
                        self.bot.debug_mode = False

                    em.description = f"{ctx.author.mention} updated \"{option}\" to \"{new_value}\".\n`Original value: {original}`"
                    em.color = 0x00FF00

                elif new_value:
                    em.description = f"An improper value was passed.\n`Valid responses for {option}: [True], [False]`"
                    em.color = 0xFF0000

                elif not new_value:
                    em.description = f"The current value for {option} is:\n`{self.bot.debug_mode}`"
                    em.color = 0x0000FF

            elif option == "tz":
                if new_value in ["EST", "CST", "UTC"]:
                    original = deepcopy(self.bot.tz)
                    self.bot.tz = new_value

                    em.description = f"{ctx.author.mention} updated \"{option}\" to \"{new_value}\".\n`Original value: {original}`"
                    em.color = 0x00FF00

                elif new_value:
                    em.description = f"An improper value was passed.\n`Valid responses for {option}: [EST], [CST], [UTC]`"
                    em.color = 0xFF0000

                elif not new_value:
                    em.description = f"The current value for {option} is:\n`{self.bot.tz}`"
                    em.color = 0x0000FF

            elif option == "prefix":
                original = deepcopy(self.bot.command_prefix)
                self.bot.command_prefix = new_value

                em.description = f"{ctx.author.mention} updated \"{option}\" to \"{new_value}\".\n`Original value: {original}`"
                em.color = 0x00FF00

            elif not new_value:
                em.description = f"The current value for {option} is:\n`{self.bot.command_prefix}`"
                em.color = 0x0000FF

            else:
                em.description = f"Bot configuration option not found."
                em.color = 0x000000

        if not option:
            em.description = f"The options and values are listed below:\n" \
                             f"```debug_mode: {self.bot.debug_mode}\n" \
                             f"auto_pull: {self.bot.auto_pull}\n" \
                             f"tz: {self.bot.tz}\n" \
                             f"prefix: {self.bot.command_prefix}```"
            em.color = 0x0000FF

        await ctx.send(embed=em)
            
    @command(name="logout")
    @is_owner()
    async def blogout(self, ctx: Context):
        await ctx.send("Logging out...")
        if not exists(join(self.bot.cwd, "Serialized", "data.pkl")):
            await ctx.send("[Unable to save] data.pkl not found. Replace file before shutting down.")
            print("[Unable to save] data.pkl not found. Replace file before shutting down.")
            return

        print("Saving files and awaiting logout...")
        with open(join(self.bot.cwd, "Serialized", "data.pkl"), "wb") as f:
            try:
                data = {
                    "Directories": self.bot.univ.Directories

                }

                dump(data, f)
            except Exception as e:
                await ctx.send(f"[Unable to save; Data Reset] Pickle dumping Error: {e}")

        with suppress(Exception):  # Comment this out and unindent logout() to disable suppressing
            await self.bot.logout()


def setup(bot: Bot):
    """Admin"""
    bot.add_cog(Admin(bot))
