import os, random, asyncio, traceback, sys

from typing import Optional
from platform import commands, tasks

import platform

from config.config import Configuration
from database.db import Database


class PIBot(commands.Bot):  # discord.Client
    def __init__(self, **kwargs):
        super().__init__(command_prefix=self.__get_prefix, intents=discord.Intents.all())
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        # self.tree = app_commands.CommandTree(self)
        self.database = Database()  # - Assign database object to client for easy SQL queries -
        self.configuration = Configuration(["general", "client"])
        self.restrictGuild = self.__restrict_guild()
        self.synced_views = False

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):  # - Guilds restrict is not working for now -
        # This copies the global commands over to your guild.
        # self.tree.copy_global_to(guild=self.restrictGuild)
        # await self.tree.sync(guild=self.restrictGuild)
        self.tree.copy_global_to(guild=self.restrictGuild)
        await self.tree.sync()

    def __restrict_guild(self):
        guild_id = self.configuration.get(category="overview", key="developer.commands.restrict_to")
        return discord.Object(id=guild_id)

    def __get_prefix(self, client, message: discord.Message):
        try:
            prefix = self.database.selectone(table='guilds.properties', columns=['prefix'],
                                             condition={"id": message.guild.id});
            prefix = prefix
        except Exception as e:
            prefix = self.configuration.read(category="utilities", key="database.defaults.prefix");
            self.log.exception(f'Error while getting prefix: {getattr(e, "message", repr(e))}');
        return prefix;

    # @util.dependencies("cogs.tickets.TicketView") # - not working -
    def __sync_views(self):
        from views.tickets import TicketLaunchView, TicketManageView

        if not self.synced_views:
            self.add_view(TicketLaunchView())
            self.add_view(TicketManageView())
            self.synced_views = True
            self.log.notify(f"Views resynced");
        else:
            pass

    async def on_ready(self):  # - TODO: Optimize json file data fetch by making less connections -
        try:
            statuses = {"online": discord.Status.online, "offline": discord.Status.offline, "idle": discord.Status.idle,
                        "dnd": discord.Status.dnd}  # - statuses available to be set as bot's status in discord -
            activitiesList = {"watching": discord.ActivityType.watching,
                              "listening": discord.ActivityType.listening}  # - Available activities types, `playing` not included due to diffrent setup procedure -
            if self.configuration.read(category="overview", key="developer.active"):
                status = self.configuration.read(category="overview", key="developer.discord-status")
                if status not in list(statuses.keys()):
                    raise ValueError("`{}` status is not supported, try instead: {}".format(status, ', '.join(
                        list(statuses.keys()))));
                status = statuses[status]
            elif self.configuration.read(category="overview", key="discord.status.set") not in list(
                    statuses.keys()):  # - Checking if status given in json file is correct for use, assigning python code if apply, set to online if not. -
                raise ValueError("`{}` status is not supported, try instead: {}".format(
                    self.configuration.read(category="overview", key="discord.status.set"),
                    ', '.join(list(statuses.keys()))));
            else:
                status = statuses[self.configuration.read(category="overview", key="discord.status.set")];
            # - End of custom status assign. -

            # - Assingning custom activity status to bot -
            activity = ''
            if self.configuration.read(category="overview", key="discord.activity.set"):
                activities = self.configuration.read(category="overview", key="discord.activity.list");
                pool = self.configuration.read(category="overview", key="discord.activity.pool");
                if self.configuration.read(category="overview", key="developer.active"):
                    activities = self.configuration.read(category="overview", key="developer.discord-custom-sctivity");
                elif activities == 'random':  # - Random list means random choice of available lists. -
                    activities = pool[random.choice(list(pool.keys()))];
                elif activities in list(pool.keys()):
                    activities = pool[activities];
                else:
                    raise ValueError("`{}` activities list not found".format(activities));
                if len(activities['list']) == 0:
                    raise ValueError("List of custom statuses can not be empty, set activity to false in such case");
                activity = random.choice(activities['list']).format(
                    guildsCount=str(len([guild.id for guild in self.guilds])),
                    membersCount=str(sum([len([m for m in guild.members if not m.bot]) for guild in self.guilds])),
                    helpCommand='/help')
                if activities[
                    'type'] == 'playing':  # - Set special statuses: 'Playing something' or 'Watching something' etc. -
                    await self.change_presence(status=status, activity=discord.Game(activity));
                elif activities['type'] in list(activitiesList.keys()):
                    await self.change_presence(status=status,
                                               activity=discord.Activity(type=activitiesList[activities['type']],
                                                                         name=activity));
                else:
                    raise ValueError("{} is not a valid activity type".format(activities['type']));
            else:
                await self.change_presence(status=status,
                                           activity=None);  # - Change only status if activities are not meant to be set -

            self.__sync_views()  # - Add views after restart, making them work -

            self.log.hard('- - - - - - - - - - - APPLICATION ONLINE - - - - - - - - - - -')
            self.log.notify(
                '{} guilds; status: {}; activity: {}'.format(str(len([guild.id for guild in self.guilds])), status,
                                                             activity if activity else 'None'))
            if self.configuration.read(category="overview", key="discord.activity.set") and self.configuration.read(
                    category="overview", key="discord.activity.cycle"):
                self.log.notify("Activity changing from pool: {} in interval: {}".format(', '.join(activities['list']),
                                                                                         self.configuration.read(
                                                                                             category="overview",
                                                                                             key="discord.activity.cycle-interval")));
                self.loop.create_task(self.cycleStatus(activities=activities,
                                                       interval=self.configuration.read(category="overview",
                                                                                        key="discord.activity.cycle-interval"),
                                                       status=status))

        # - Sync slash commands tree to global -
        # await self.tree.sync()
        except Exception as e:
            self.log.error(getattr(e, 'message', repr(e)))
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)

    async def cycleStatus(self, activities, interval, status):
        try:
            activitiesList = {"watching": discord.ActivityType.watching,
                              "listening": discord.ActivityType.listening}  # - Available activities types, `playing` not included due to diffrent setup procedure -
            await self.wait_until_ready()
            while not self.is_closed():
                if isinstance(interval, int):
                    time = interval;
                elif interval == 'random':  # - Interval draw -
                    time = random.randint(900, 7200);
                elif interval == 'short':
                    time = random.randint(900, 2700);
                elif interval == 'long':
                    time = random.randint(2700, 7200);
                else:  # - In case of not appropriate interval given ( not: short, long, random ). -
                    raise ValueError("{} is not a valid interval".format(interval));
                activity = random.choice(activities['list']).format(
                    guildsCount=str(len([guild.id for guild in self.guilds])),
                    membersCount=str(sum([len([m for m in guild.members if not m.bot]) for guild in self.guilds])),
                    helpCommand='/help')
                self.log.notify("Next activity: {}; Waiting {} seconds.".format(activity, time))
                await asyncio.sleep(time)  # - Wait interval. -
                if activities[
                    'type'] == 'playing':  # - Set special statuses: 'Playing something' or 'Watching something' etc. -
                    await self.change_presence(status=status, activity=discord.Game(activity));
                elif activities['type'] in list(activitiesList.keys()):
                    await self.change_presence(status=status,
                                               activity=discord.Activity(type=activitiesList[activities['type']],
                                                                         name=activity));
        except Exception as error:
            self.log.error(getattr(e, 'message', repr(e)))
