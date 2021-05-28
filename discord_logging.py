import discord
from discord.ext import tasks
from config import DISCORD_CHANNELS, DISCORD_INIT, DISCORD_ACTION_MSG, DISCORD_TEST_MSG


def parse_action(action):
    return "\n\n" + DISCORD_ACTION_MSG \
          + "[{}]".format(action["type"]) + ' **' + action["title"] + '**\n' \
          + "submitted by u/" + action["author"] + "\n" \
          + action["permalink"] + "\n\n" \
          + action["comment"]


class LoggingClient(discord.Client):
    def __init__(self, logging_queue, command_queue, **options):
        super().__init__(**options)
        self.logging_queue = logging_queue
        self.command_queue = command_queue
        self.action_proc = None
        self.check_queue.start()

    async def on_ready(self):
        await self.send_to_channel(DISCORD_INIT)

    async def send_to_channel(self, msg):
        for channel in self.get_all_channels():
            if channel.name in DISCORD_CHANNELS:
                await channel.send(msg)

    @tasks.loop(seconds=1)
    async def check_queue(self):
        if not self.logging_queue.empty():
            pack = self.logging_queue.get()
            msg = None
            if type(pack) is dict:
                msg = parse_action(pack)
            elif type(pack) is str:
                msg = pack
            await self.send_to_channel(msg)

    @check_queue.before_loop
    async def pre_check(self):
        await self.wait_until_ready()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == "!test msg" and message.author.name == "LZ58840":
            await message.channel.send(DISCORD_TEST_MSG)

        if message.content.startswith("!shadow") and message.author.name == "LZ58840":
            self.command_queue.put(message.content)
