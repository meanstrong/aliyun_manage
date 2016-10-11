from web.aliyun.ecs import ECS
from web import config

from flask import Flask

__author__ = 'Rocky Peng'


app = Flask(__name__)
app.config.from_object("web.config")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


from .controller import api, aliyun
# ecs = ECS(config.AccessKey, config.AccessSecret, config.RegionId)
