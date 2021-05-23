import asyncio
import discord
from discord.ext import tasks
from config import DISCORD_CHANNELS, DISCORD_INIT, DISCORD_ACTION_MSG, DISCORD_TEST_MSG


def parse_action(action):
    return 120 * r"\_" + "\n" \
          + DISCORD_ACTION_MSG \
          + "[{}]".format(action["type"]) + ' **' + action["title"] + '**\n' \
          + "submitted by u/" + action["author"] + "\n" \
          + action["permalink"] + "\n\n" \
          + action["comment"]


class LoggingClient(discord.Client):
    def __init__(self, logging_queue, **options):
        super().__init__(**options)
        self.comm = logging_queue
        self.action_proc = None
        self.check_comm.start()

    async def on_ready(self):
        for channel in self.get_all_channels():
            if channel.name in DISCORD_CHANNELS:
                await channel.send(DISCORD_INIT)

    @tasks.loop(seconds=1)
    async def check_comm(self):
        if not self.comm.empty():
            msg = parse_action(self.comm.get())
            for channel in self.get_all_channels():
                if channel.name in DISCORD_CHANNELS:
                    await channel.send(msg)

    @check_comm.before_loop
    async def pre_check(self):
        await self.wait_until_ready()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == "!test msg" and message.author.name == "LZ58840":
            await message.channel.send(DISCORD_TEST_MSG)
