from web.aliyun.ecs import ECS
from web import config

ecs = ECS(config.AccessKey, config.AccessSecret, config.RegionId)
