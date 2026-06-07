from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, CustomTokenObtainPairView, UserProfileView

urlpatterns = [
    # 1. 注册接口: POST /api/users/register/
    path('register/', RegisterView.as_view(), name='register'),
    
    # 2. 登录接口: POST /api/users/login/ (使用我们定制的视图)
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # 3. 刷新 Token 接口: POST /api/users/token/refresh/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 4. 个人资料接口: GET/PUT /api/users/profile/
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]