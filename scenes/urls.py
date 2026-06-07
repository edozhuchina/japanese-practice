from django.urls import path
from .views import SceneListView, SceneDetailView, ProgressView, CompleteDialogueView

urlpatterns = [
    path('', SceneListView.as_view(), name='scene-list'),
    path('<int:pk>/', SceneDetailView.as_view(), name='scene-detail'),
    path('progress/', ProgressView.as_view(), name='scene-progress'),
    path('complete/', CompleteDialogueView.as_view(), name='scene-complete'),
]
