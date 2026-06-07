from django.contrib import admin
from .models import Scene, Dialogue, StudyProgress


class DialogueInline(admin.TabularInline):
    model = Dialogue
    extra = 0
    fields = ('role', 'japanese_text', 'kana_text', 'romaji_text', 'chinese_text', 'order')
    ordering = ('order',)


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'is_active', 'created_at')
    list_filter = ('category', 'level', 'is_active')
    search_fields = ('title', 'description')
    inlines = [DialogueInline]
    ordering = ('-created_at',)


@admin.register(Dialogue)
class DialogueAdmin(admin.ModelAdmin):
    list_display = ('scene', 'role', 'japanese_text', 'kana_text', 'order')
    list_filter = ('scene', 'role')
    search_fields = ('japanese_text', 'kana_text', 'chinese_text')


@admin.register(StudyProgress)
class StudyProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'scene', 'dialogue', 'is_completed', 'is_marked', 'completed_at')
    list_filter = ('is_completed', 'is_marked')
    search_fields = ('user__username', 'scene__title')
    readonly_fields = ('completed_at',)
