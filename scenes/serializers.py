from rest_framework import serializers
from .models import Scene, Dialogue, StudyProgress

# 1. 对话句子序列化器
class DialogueSerializer(serializers.ModelSerializer):
    # 自动把 'A' 或 'B' 转换成人类可读的 "角色A" 或 "角色B"
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = Dialogue
        fields = [
            'id', 'role', 'role_display', 'japanese_text', 
            'kana_text', 'romaji_text', 'chinese_text', 
            'audio_url', 'vocabulary', 'order'
        ]

# 2. 场景列表序列化器 (轻量级，不包含具体对话，用于首页展示卡片)
class SceneListSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    # 统计这个场景下有多少句对话
    dialogue_count = serializers.SerializerMethodField() 

    class Meta:
        model = Scene
        fields = [
            'id', 'title', 'description', 'category', 'category_display', 
            'level', 'level_display', 'cover_image', 'dialogue_count'
        ]

    def get_dialogue_count(self, obj):
        return obj.dialogues.count()

# 3. 场景详情序列化器 (重量级，包含所有对话句子)
class SceneDetailSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    
    # ⬇️ 核心：嵌套查询。因为模型里设置了 related_name='dialogues'
    # many=True 表示这是一对多关系，read_only=True 表示只读
    dialogues = DialogueSerializer(many=True, read_only=True) 

    class Meta:
        model = Scene
        fields = [
            'id', 'title', 'description', 'category', 'category_display', 
            'level', 'level_display', 'cover_image', 'dialogues'
        ]
# 4. 学习进度序列化器
class StudyProgressSerializer(serializers.ModelSerializer):
    scene_title = serializers.CharField(source='scene.title', read_only=True)
    dialogue_text = serializers.CharField(source='dialogue.japanese_text', read_only=True)

    class Meta:
        model = StudyProgress
        fields = ['id', 'scene_title', 'dialogue_text', 'is_completed', 'is_marked', 'completed_at']
        read_only_fields = ['id', 'completed_at']
