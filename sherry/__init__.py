import jinja2
from flask import Flask
import os

import log

app = Flask(__name__)
app.config.from_object('sherry.settings_default')
# Load from the environment variable if defined
app.config.from_envvar('SHERRY_SETTINGS_PATH', silent=True)

app.jinja_env.undefined = jinja2.StrictUndefined

app.logger.addHandler(app.config['LOG_HANDLER'])
app.memory_log = log.RollingMemoryHandler(max_records=50)
app.logger.addHandler(app.memory_log)
import sherry.views
