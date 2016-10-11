# -*- coding:utf-8 -*-
import time
import json
import subprocess
import paramiko

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest, \
    DescribeZonesRequest, CreateInstanceRequest, DescribeImagesRequest, \
    DescribeInstanceTypesRequest, DescribeInstancesRequest, \
    DeleteInstanceRequest, StartInstanceRequest, StopInstanceRequest, \
    AllocatePublicIpAddressRequest, DescribeInstanceVncUrlRequest, \
    DescribeInstanceStatusRequest

from web import config

__author__ = 'Rocky Peng'


class ECS(object):

    def __init__(self, access_key, access_secret, region_id):
        self.access_key = access_key
        self.access_secret = access_secret
        self.region_id = region_id

    def DescribeRegions(self):
        '''查询可用地域列表
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format("json")
        result = clt.do_action(request)
        return json.loads(result)

    def DescribeZones(self):
        '''查询可用区
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DescribeZonesRequest.DescribeZonesRequest()
        request.set_accept_format("json")
        result = clt.do_action(request)
        return json.loads(result)

    def DescribeImages(self):
        '''查询可用镜像
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DescribeImagesRequest.DescribeImagesRequest()
        request.set_accept_format("json")
        result = clt.do_action(request)
        return json.loads(result)

    def DescribeInstanceTypes(self):
        '''查询实例资源规格列表
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        request.set_accept_format("json")
        result = clt.do_action(request)
        return json.loads(result)

    def CreateInstance(self):
        '''创建实例
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_accept_format("json")
        request.set_ImageId(config.DefaultImageId)
        request.set_InstanceType(config.DefaultInstanceType)
        request.set_InstanceChargeType("PostPaid")
        request.set_InternetChargeType("PayByTraffic")
        request.set_InternetMaxBandwidthIn(1)
        request.set_InternetMaxBandwidthOut(1)
        request.set_Password(config.DefaultPassword)
        result = clt.do_action(request)
        result = json.loads(result)
        if not result.get("Code"):
            InstanceId = result["InstanceId"]
            self.AllocatePublicIpAddress(InstanceId)
        return result

    def DescribeInstances(self):
        '''查询实例列表
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format("json")
        result = clt.do_action(request)
        return json.loads(result)

    def DeleteInstance(self, InstanceId):
        '''删除实例
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DeleteInstanceRequest.DeleteInstanceRequest()
        request.set_accept_format("json")
        request.set_InstanceId(InstanceId)
        result = clt.do_action(request)
        return json.loads(result)

    def DeleteAllInstances(self):
        '''删除所有实例
        '''
        instances = self.DescribeInstances()
        if instances.get("Code"):
            raise Exception("DescribeInstances Error: %s" % instances.get("Message"))
        for instance in instances["Instances"]["Instance"]:
            self.DeleteInstance(instance["InstanceId"])

    def StopInstance(self, InstanceId, ForceStop=True):
        '''停止实例
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = StopInstanceRequest.StopInstanceRequest()
        request.set_accept_format("json")
        request.set_InstanceId(InstanceId)
        if ForceStop:
            request.set_ForceStop("true")
        result = clt.do_action(request)
        return json.loads(result)

    def StartInstance(self, InstanceId):
        '''启动实例
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = StartInstanceRequest.StartInstanceRequest()
        request.set_accept_format("json")
        request.set_InstanceId(InstanceId)
        result = clt.do_action(request)
        return json.loads(result)

    def DescribeInstanceStatus(self):
        '''查询实例状态
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
        request.set_accept_format("json")
        result = clt.do_action(request)
        return json.loads(result)

    def AllocatePublicIpAddress(self, InstanceId):
        '''分配公网 IP 地址
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
        request.set_accept_format("json")
        request.set_InstanceId(InstanceId)
        result = clt.do_action(request)
        return json.loads(result)

    def DescribeInstanceVncUrl(self, InstanceId):
        '''查询实例管理终端地址
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DescribeInstanceVncUrlRequest.DescribeInstanceVncUrlRequest()
        request.set_accept_format("json")
        request.set_InstanceId(InstanceId)
        result = clt.do_action(request)
        return json.loads(result)

    def SendFile(self, InstanceId, src, dest):
        '''向实例发送文件到指定路径下
        '''
        result = self.AllocatePublicIpAddress(InstanceId)
        if result.get("Code"):
            raise Exception("AllocatePublicIpAddress Error: %s" % result.get("Message"))
        ip = result["IpAddress"]
        cmd = ("rsync -avzq --rsh=\"sshpass -p "+
            config.DefaultPassword+
            " ssh -p 22\" "+src+" root@"+ip+":"+dest)
        print cmd
        process = subprocess.Popen(cmd, shell=True)
        rc = process.poll()
        if rc:
            raise Exception("send file Error")

    def ExecCommand(self, InstanceId, shell):
        '''在实例上执行shell
        '''
        result = self.AllocatePublicIpAddress(InstanceId)
        if result.get("Code"):
            raise Exception("AllocatePublicIpAddress Error: %s" % result.get("Message"))
        ip = result["IpAddress"]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, "root", config.DefaultPassword, timeout=10)
        chan = ssh.get_transport().open_session()
        chan.exec_command(shell)
        buff_size = 1024
        stdout = ""
        stderr = ""
        while not chan.exit_status_ready():
            time.sleep(1)
            if chan.recv_ready():
                stdout += chan.recv(buff_size)
            if chan.recv_stderr_ready():
                stderr += chan.recv_stderr(buff_size)
        rc = chan.recv_exit_status()
        while chan.recv_ready():
            stdout += chan.recv(buff_size)
        while chan.recv_stderr_ready():
            stderr += chan.recv_stderr(buff_size)
        return dict(rc=rc, stdout=stdout, stderr=stderr)
