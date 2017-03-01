# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.utils.functional import lazy

GENDER_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
)
PROVINCE_CHOICES = (
    (None, '----'),
    (34, '安徽'),
    (11, '北京'),
    (50, '重庆'),
    (35, '福建'),
    (62, '甘肃'),
    (44, '广东'),
    (45, '广西'),
    (52, '贵州'),
    (46, '海南'),
    (13, '河北'),
    (23, '黑龙江'),
    (41, '河南'),
    (42, '湖北'),
    (43, '湖南'),
    (15, '内蒙古'),
    (32, '江苏'),
    (36, '江西'),
    (22, '吉林'),
    (21, '辽宁'),
    (64, '宁夏'),
    (63, '青海'),
    (14, '山西'),
    (37, '山东'),
    (31, '上海'),
    (51, '四川'),
    (14, '山西'),
    (37, '山东'),
    (31, '上海'),
    (51, '四川'),
    (12, '天津'),    
    (54, '西藏'),
    (65, '新疆'),
    (53, '云南'),
    (33, '浙江'),
    (61, '陕西'),
    (71, '台湾'),
    (81, '香港'),
    (82, '澳门'),
    (400, '海外'),
    (100, '其他'),
)
CITY_CHOICES = (
    ('43', (
            (1, '长沙'),
            (2, '株洲'),
            (3, '湘潭'),
            (4, '衡阳'),
            (5, '邵阳'),
            (6, '岳阳'),
            (7, '常德'),
            (8, '张家界'),
            (9, '益阳'),
            (10, '郴州'),
            (11, '永州'),
            (12, '怀化'),
            (13, '娄底'),
            (31, '湘西土家族苗族自治州'),
        )
    )
)
class WeiboUser(models.Model):
    weibo_id = models.BigIntegerField(null=True, blank=True, unique=True)
    weibo_name = models.CharField('weibo name', max_length=40, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    province = models.PositiveSmallIntegerField(null=True, blank=True, choices=PROVINCE_CHOICES)
    city = models.PositiveSmallIntegerField(null=True, blank=True)
    location = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        verbose_name = 'weibo user'
        verbose_name_plural = 'weibo users'

    def __unicode__(self):
        return '%s' % (self.weibo_id,)
