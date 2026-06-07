from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

# ================= 1. 注册序列化器 =================
class UserRegistrationSerializer(serializers.ModelSerializer):
    """处理用户注册逻辑"""
    # write_only=True 表示前端传过来，但后端返回时不会包含密码
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password], # 使用 Django 内置的密码强度校验
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True, 
        label="确认密码",
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        # 包含我们自定义模型中的专属字段
        fields = (
            'username', 'password', 'password2', 'email', 
            'nickname', 'japanese_level', 'learning_goal'
        )

    def validate(self, attrs):
        """验证两次输入的密码是否一致"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "两次输入的密码不一致！"})
        return attrs

    def create(self, validated_data):
        """重写创建方法，确保密码被哈希加密"""
        # 弹出 password2，因为数据库里没有这个字段
        validated_data.pop('password2')
        
        # ⚠️ 核心：必须使用 create_user，它会自动处理密码加密
        user = User.objects.create_user(**validated_data)
        return user


# ================= 2. 登录序列化器 (深度定制) =================
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    定制 JWT 登录返回数据
    默认只返回 access 和 refresh，我们在这里把用户信息也塞进去，减少前端请求次数
    """
    def validate(self, attrs):
        # 调用父类方法，验证用户名密码并生成 token
        data = super().validate(attrs)
        
        # 将当前登录用户的信息附加到返回的 JSON 中
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'nickname': self.user.nickname if self.user.nickname else self.user.username,
            'avatar': self.user.avatar,
            'japanese_level': self.user.japanese_level,
            'learning_goal': self.user.learning_goal,
        }
        return data


# ================= 3. 用户信息展示与更新序列化器 =================
class UserProfileSerializer(serializers.ModelSerializer):
    """处理获取和修改个人资料"""
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'nickname', 'avatar', 
            'japanese_level', 'learning_goal', 'last_active', 'date_joined'
        )
        # 这些字段不允许前端通过 API 随意修改
        read_only_fields = ('id', 'username', 'last_active', 'date_joined')