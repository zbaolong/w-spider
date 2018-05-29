# encoding:utf-8
from util.RespEntity import RespEntity

def InstanceNotFoundError():
    return RespEntity.error(404,"Instance Not Found"),404

def InstanceExistsError():
    return RespEntity.error(400,"Instance Exists Error"),400