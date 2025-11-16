from rest_framework import serializers
from apps.answers.models import Answer


class AnswerCreateSerialier(serializers.ModelSerializer[Answer]):
    class Meta:
        model = Answer
        fields = ['user_id', 'text']

    def validate_user_id(self, value:str) -> str:
        """Валидация user_id - принимаем любой идентификатор пользователя"""
        if not value:
            raise serializers.ValidationError("User ID не может быть пустым")
        
        if len(value) > 36:
            raise serializers.ValidationError("User ID слишком длинный")
        
        return value
    
    def validate_text(self, value:str) -> str:
        if not value or not value.strip():
            raise serializers.ValidationError("Текст ответа отсутствует")
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Текст ответа слишком короткий")
        if len(value) > 2000:
            raise serializers.ValidationError("Текст ответа слишком длинный")
        return value.strip()
    

class AnswerSerializer(serializers.ModelSerializer[Answer]):
    question_id = serializers.IntegerField(source="question.id", read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'question_id', 'user_id', 'text', 'created_at']
