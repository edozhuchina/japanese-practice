# Create your models here.
from django.db import models

class Scene(models.Model):
    """
    场景模型 (例如：居酒屋点单、便利店购物)
    """
    CATEGORY_CHOICES = [
        ('food', '餐饮美食'),
        ('travel', '交通出行'),
        ('shopping', '购物血拼'),
        ('daily', '日常生活'),
        ('business', '商务职场'),
    ]
    
    LEVEL_CHOICES = [
        ('N5', 'N5 (入门)'),
        ('N4', 'N4 (基础)'),
        ('N3', 'N3 (进阶)'),
        ('N2', 'N2 (中高级)'),
        ('N1', 'N1 (高级)'),
    ]

    title = models.CharField(max_length=100, verbose_name="场景标题")
    description = models.TextField(blank=True, default='', verbose_name="场景描述/背景介绍")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='daily', verbose_name="场景分类")
    level = models.CharField(max_length=5, choices=LEVEL_CHOICES, default='N5', verbose_name="难度等级")
    cover_image = models.URLField(max_length=500, blank=True, default='', verbose_name="封面图URL")
    
    is_active = models.BooleanField(default=True, verbose_name="是否上线")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "学习场景"
        verbose_name_plural = "学习场景"
        ordering = ['-created_at'] # 最新创建的排在前面

    def __str__(self):
        return f"[{self.get_level_display()}] {self.title}"


class Dialogue(models.Model):
    """
    对话句子模型 (属于某个具体的 Scene)
    """
    ROLE_CHOICES = [
        ('A', '角色A (如：顾客/提问者)'),
        ('B', '角色B (如：店员/回答者)'),
    ]

    scene = models.ForeignKey(
        Scene, 
        on_delete=models.CASCADE, 
        related_name='dialogues', # ⬅️ 核心：允许通过 scene.dialogues.all() 反向查询所有句子
        verbose_name="所属场景"
    )
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='A', verbose_name="说话角色")
    
    # 🌟 日语学习专属字段
    japanese_text = models.CharField(max_length=255, verbose_name="日文原文")
    kana_text = models.CharField(max_length=255, blank=True, default='', verbose_name="平假名注音 (Furigana)")
    romaji_text = models.CharField(max_length=255, blank=True, default='', verbose_name="罗马音")
    chinese_text = models.CharField(max_length=255, verbose_name="中文翻译")
    
    audio_url = models.URLField(max_length=500, blank=True, default='', verbose_name="发音音频URL")
    
    # 语法点或重点词汇，用 JSON 格式存储，方便前端解析
    # 例如: [{"word": "すみません", "meaning": "不好意思/打扰一下"}]
    vocabulary = models.JSONField(default=list, blank=True, verbose_name="核心词汇/语法点") 
    
    order = models.PositiveIntegerField(default=1, verbose_name="对话顺序")

    class Meta:
        verbose_name = "对话句子"
        verbose_name_plural = "对话句子"
        ordering = ['scene', 'order'] # 先按场景分组，再按顺序排列

    def __str__(self):
        return f"{self.get_role_display()}: {self.japanese_text}"

class StudyProgress(models.Model):
    """
    学习进度模型：记录每个用户对每个场景的练习进度
    """
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='study_progress',
        verbose_name="用户"
    )
    scene = models.ForeignKey(
        Scene, 
        on_delete=models.CASCADE, 
        related_name='study_progress',
        verbose_name="场景"
    )
    dialogue = models.ForeignKey(
        Dialogue,
        on_delete=models.CASCADE,
        related_name='study_progress',
        verbose_name="对话"
    )
    is_completed = models.BooleanField(default=False, verbose_name="是否完成")
    is_marked = models.BooleanField(default=False, verbose_name="是否标记为难点")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="完成时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "学习进度"
        verbose_name_plural = "学习进度"
        unique_together = ('user', 'dialogue')  # 同一用户对同一对话只有一条记录
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.scene.title} - {self.dialogue.japanese_text[:20]}"
