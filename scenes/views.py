# Create your views here.
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.utils import timezone
from .models import Scene, StudyProgress
from .serializers import SceneListSerializer, SceneDetailSerializer, StudyProgressSerializer


class SceneListView(generics.ListAPIView):
    """
    获取场景列表
    支持按分类和难度过滤 (例如: ?category=food&level=N5)
    """
    queryset = Scene.objects.filter(is_active=True)
    serializer_class = SceneListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'level']


class SceneDetailView(generics.RetrieveAPIView):
    """
    获取单个场景的详情 (包含所有对话句子)
    URL: /api/scenes/<id>/
    """
    queryset = Scene.objects.filter(is_active=True)
    serializer_class = SceneDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProgressView(generics.ListAPIView):
    """
    获取当前用户某个场景的学习进度
    GET /api/scenes/progress/?scene_id=1
    """
    serializer_class = StudyProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        scene_id = self.request.query_params.get('scene_id')
        if not scene_id:
            return StudyProgress.objects.none()
        return StudyProgress.objects.filter(
            user=self.request.user,
            scene_id=scene_id
        )
    
    def list(self, request, *args, **kwargs):
        progress_list = self.get_queryset()
        completed_ids = [p.dialogue_id for p in progress_list if p.is_completed]
        marked_ids = [p.dialogue_id for p in progress_list if p.is_marked]
        
        return Response({
            'completed_dialogues': completed_ids,
            'marked_dialogues': marked_ids,
            'total_completed': len(completed_ids)
        })


class CompleteDialogueView(generics.GenericAPIView):
    """
    标记对话完成或标记为难点
    POST /api/scenes/complete/
    Body: {"scene_id": 1, "dialogue_id": 5, "marked": false}
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        scene_id = request.data.get('scene_id')
        dialogue_id = request.data.get('dialogue_id')
        marked = request.data.get('marked', False)
        
        if not scene_id or not dialogue_id:
            return Response(
                {'error': '需要提供 scene_id 和 dialogue_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        progress, created = StudyProgress.objects.get_or_create(
            user=request.user,
            scene_id=scene_id,
            dialogue_id=dialogue_id,
            defaults={'is_marked': marked}
        )
        
        progress.is_marked = marked
        if marked:
            progress.is_completed = True
            progress.completed_at = timezone.now()
        elif progress.is_completed:
            progress.is_completed = False
            progress.completed_at = None
        progress.save()
        
        return Response({
            'message': '进度已更新',
            'is_completed': progress.is_completed,
            'is_marked': progress.is_marked
        }, status=status.HTTP_200_OK)
