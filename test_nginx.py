# -*- coding:utf-8 -*-
import time

from web.aliyun.ecs import ECS
from web import config


ecs = ECS(config.AccessKey, config.AccessSecret, config.RegionId)
result = ecs.CreateInstance()
if result.get("Code"):
    raise Exception("CreateInstance")
InstanceId = result["InstanceId"]

result = ecs.StartInstance(InstanceId)
if result.get("Code"):
    raise Exception("StartInstance")

while 1:
    result = ecs.DescribeInstanceStatus()
    if result.get("Code"):
        raise Exception("DescribeInstanceStatus")
    status = ""
    for instance in result["InstanceStatuses"]["InstanceStatus"]:
        if instance["InstanceId"] == InstanceId:
            status = instance["Status"]
    if status == "Running":
        print("instance running OK.")
        break
    else:
        print("instance not running[%s], next query." % status)
    time.sleep(3)

for i in range(60):
    try:
        ecs.ExecCommand(InstanceId, "ls")
    except Exception:
        print("wait for instance sshd running.")
        time.sleep(3)
    else:
        break

ecs.ExecCommand(InstanceId, "apt-get update")
ecs.ExecCommand(InstanceId, "apt-get install nginx -y")
print("instance nginx install OK.")
result = ecs.AllocatePublicIpAddress(InstanceId)
if result.get("Code"):
    raise Exception("AllocatePublicIpAddress Error")
print("Now you can visit \"http://%s\"" % result["IpAddress"])
