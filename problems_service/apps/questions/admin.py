from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_preview', 'answers_count', 'created_at')
    list_display_links = ('id', 'text_preview')
    list_filter = ('created_at',)
    search_fields = ('text',)
    readonly_fields = ('created_at', 'answers_count')
    fieldsets = (
        (None, {
            'fields': ('text', 'created_at')
        }),
        ('Статистика', {
            'fields': ('answers_count',),
            'classes': ('collapse',)
        }),
    )

    def text_preview(self, obj):
        """Превью текста вопроса"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст вопроса'

    def answers_count(self, obj):
        """Количество ответов на вопрос"""
        return obj.answers.count()
    answers_count.short_description = 'Количество ответов'

    def get_queryset(self, request):
        """Оптимизация запроса с подсчетом ответов"""
        return super().get_queryset(request).prefetch_related('answers')