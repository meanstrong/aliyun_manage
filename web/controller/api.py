# -*- coding:utf-8 -*-
from flask import request, jsonify, g

from web import app
from web import config
from web.aliyun.ecs import ECS

__author__ = 'Rocky Peng'
ecs = ECS(config.AccessKey, config.AccessSecret, config.RegionId)

@app.route("/api/aliyun", methods=["GET"])
def Aliyun():
    action = request.args.get("Action")
    if action == "CreateInstance":
        result = ecs.CreateInstance()
    elif action == "DescribeInstances":
        result = ecs.DescribeInstances()
    elif action == "StartInstance":
        instance_id = request.args.get("InstanceId")
        result = ecs.StartInstance(instance_id)
    elif action == "StopInstance":
        instance_id = request.args.get("InstanceId")
        result = ecs.StopInstance(instance_id)
    elif action == "DeleteInstance":
        instance_id = request.args.get("InstanceId")
        result = ecs.DeleteInstance(instance_id)
    elif action == "DescribeInstanceVncUrl":
        instance_id = request.args.get("InstanceId")
        result = ecs.DescribeInstanceVncUrl(instance_id)
    return jsonify(result)

@app.route("/api/aliyun/exec_command", methods=["POST"])
def ExecCommand():
    instance_id = request.args.get("InstanceId")
    command = request.form.get("command")
    result = ecs.ExecCommand(instance_id, command)
    return jsonify(result)
