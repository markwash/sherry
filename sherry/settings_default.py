DEBUG = False

# Is this a good hack? A bad one? It's a bit weird...
from sherry.power import MockPowerDriver as POWER_DRIVER

TEST_IMAGE_LOCATION = 'test'

from logging import StreamHandler
LOG_HANDLER = StreamHandler()
