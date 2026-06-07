# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import (
    UserRegistrationSerializer, 
    CustomTokenObtainPairSerializer, 
    UserProfileSerializer
)

User = get_user_model()

# ================= 1. 注册 API =================
class RegisterView(generics.CreateAPIView):
    """用户注册接口"""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,) # 允许任何人（未登录）访问
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        # 如果数据不合法（如用户名已存在、密码太弱），这里会自动抛出 400 错误
        serializer.is_valid(raise_exception=True) 
        user = serializer.save()
        
        # 返回友好的成功提示
        return Response({
            "code": 201,
            "message": "注册成功！欢迎加入日语学习之旅，请登录。",
            "data": {
                "username": user.username,
                "nickname": user.nickname
            }
        }, status=status.HTTP_201_CREATED)


# ================= 2. 登录 API (使用定制版) =================
class CustomTokenObtainPairView(TokenObtainPairView):
    """用户登录接口 (返回 Token + 用户信息)"""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (permissions.AllowAny,)


# ================= 3. 获取/更新个人资料 API =================
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    获取或更新当前登录用户的资料
    GET: 获取资料
    PUT/PATCH: 修改资料 (如修改昵称、更新日语等级)
    """
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,) # 必须登录才能访问

    def get_object(self):
        """
        重写此方法：不需要在 URL 中传 user_id，
        直接根据请求头中的 JWT Token 自动识别并返回当前用户
        """
        return self.request.user