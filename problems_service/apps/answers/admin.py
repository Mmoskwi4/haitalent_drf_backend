from django.contrib import admin
from .models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_preview', 'user_id', 'text_preview', 'created_at')
    list_display_links = ('id', 'text_preview')
    list_filter = ('created_at', 'question')
    search_fields = ('text', 'user_id', 'question__text')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('question', 'user_id', 'text')
        }),
        ('Даты', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def text_preview(self, obj):
        """Превью текста ответа"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст ответа'

    def question_preview(self, obj):
        """Превью вопроса"""
        return obj.question.text[:50] + '...' if len(obj.question.text) > 50 else obj.question.text
    question_preview.short_description = 'Вопрос'

    def get_queryset(self, request):
        """Оптимизация запроса с предзагрузкой вопроса"""
        return super().get_queryset(request).select_related('question')