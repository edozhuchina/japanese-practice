# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    自定义用户模型
    继承 AbstractUser 保留了 Django 原有的 username, password, email, is_staff, is_active 等核心字段
    """
    
    # ================= 1. 基础个人信息 =================
    nickname = models.CharField(
        max_length=50, 
        blank=True, 
        default='', 
        verbose_name="昵称"
    )
    avatar = models.URLField(
        max_length=500, 
        blank=True, 
        default='', 
        verbose_name="头像URL"
    )
    
    # ================= 2. 日语学习专属画像 =================
    LEVEL_CHOICES = [
        ('zero', '零基础'),
        ('N5', 'N5 (入门)'),
        ('N4', 'N4 (基础)'),
        ('N3', 'N3 (进阶)'),
        ('N2', 'N2 (中高级)'),
        ('N1', 'N1 (高级)'),
    ]
    japanese_level = models.CharField(
        max_length=10, 
        choices=LEVEL_CHOICES, 
        default='zero',
        verbose_name="当前日语水平"
    )
    
    GOAL_CHOICES = [
        ('daily', '日常会话/旅游'),
        ('jlpt', 'JLPT 考级'),
        ('business', '商务/工作'),
        ('anime', '动漫/兴趣'),
        ('study_abroad', '留学'),
    ]
    learning_goal = models.CharField(
        max_length=20,
        choices=GOAL_CHOICES,
        default='daily',
        verbose_name="主要学习目标"
    )

    # 记录用户最后一次活跃时间，后期可用于计算“连续打卡天数”或“休眠用户唤醒”
    last_active = models.DateTimeField(
        auto_now=True, 
        verbose_name="最后活跃时间"
    )

    # ================= 3. Meta 元数据配置 =================
    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        ordering = ['-date_joined']  # 默认按注册时间倒序排列

    def __str__(self):
        # 在 Django Admin 后台显示时，优先显示昵称，没有昵称则显示用户名
        return self.nickname if self.nickname else self.username