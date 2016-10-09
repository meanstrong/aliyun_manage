# -*- coding:utf-8 -*-
import json
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest, \
    DescribeZonesRequest, CreateInstanceRequest, DescribeImagesRequest, \
    DescribeInstanceTypesRequest, DescribeInstancesRequest, \
    DeleteInstanceRequest

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
        return result

    def DescribeZones(self):
        '''查询可用区
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DescribeZonesRequest.DescribeZonesRequest()
        request.set_accept_format("json")
        result = clt.do_action(request)
        return result

    def DescribeImages(self):
        '''查询可用镜像
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DescribeImagesRequest.DescribeImagesRequest()
        request.set_accept_format("json")
        result = clt.do_action(request)
        return result

    def DescribeInstanceTypes(self):
        '''查询实例资源规格列表
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        request.set_accept_format("json")
        result = clt.do_action(request)
        return result

    def CreateInstance(self):
        '''创建实例
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_accept_format("json")
        request.set_ImageId("ubuntu1404_64_40G_cloudinit_20160727.raw")
        request.set_InstanceType("ecs.t1.small")
        request.set_InstanceChargeType("PostPaid")
        result = clt.do_action(request)
        return result

    def DescribeInstances(self):
        '''查询实例列表
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format("json")
        result = clt.do_action(request)
        return result

    def DeleteInstance(self, InstanceId):
        '''删除实例
        '''
        clt = client.AcsClient(self.access_key, self.access_secret, self.region_id)
        request = DeleteInstanceRequest.DeleteInstanceRequest()
        request.set_accept_format("json")
        request.set_InstanceId(InstanceId)
        result = clt.do_action(request)
        return result

    def DeleteAllInstances(self):
        '''删除所有实例
        '''
        instances = json.loads(self.DescribeInstances())
        if instances.get("Code"):
            raise Exception("DescribeInstances Error: %s" % instances.get("Message"))
        for instance in instances["Instances"]["Instance"]:
            self.DeleteInstance(instance["InstanceId"])
