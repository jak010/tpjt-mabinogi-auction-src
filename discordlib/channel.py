from enum import Enum

import os
from dotenv import load_dotenv

load_dotenv()


class DiscordChannel(Enum):
    CHANNEL_1 = os.environ['DISCORD_CHANNEL_1']
    CHANNEL_2 = os.environ['DISCORD_CHANNEL_2']
