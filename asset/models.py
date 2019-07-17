from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

# Create your models here.
class Hosts(models.Model):
    name = models.CharField(max_length=128,null=False,default='')
    ip = models.GenericIPAddressField(null=False,default='0.0.0.0')
    mac = models.CharField(max_length=32,null=False,default='')
    os = models.CharField(max_length=64,null=False,default='')
    arch = models.CharField(max_length=16,null=False,default='')
    mem = models.BigIntegerField(null=False,default=0)
    cpu = models.IntegerField(null=False,default=0)
    disk = models.CharField(max_length=512,null=False,default='{}')

    sn = models.CharField(max_length=128,null=False,default='')
    user = models.CharField(max_length=128,null=False,default='')
    remark = models.TextField(null=False,default='')
    purchase_time = models.DateTimeField(null=False)
    over_insurance_time = models.DateTimeField(null=False)

    created_time = models.DateTimeField(null=False,auto_now_add=True)
    last_time = models.DateTimeField(null=False)

    @classmethod
    def create_or_replace(cls,name,ip,mac,os,arch,mem,cpu,disk):
        obj = None
        try:
            obj = cls.objects.get(ip=ip)
        except ObjectDoesNotExist as e:
            obj = cls()
            obj.ip = ip
            obj.purchase_time = timezone.now()
            obj.over_insurance_time = timezone.now()

        obj.name = name
        obj.mac = mac
        obj.os = os
        obj.arch = arch
        obj.mem = mem
        obj.cpu = cpu
        obj.disk = disk

        obj.last_time = timezone.now()
        obj.save()
        return obj