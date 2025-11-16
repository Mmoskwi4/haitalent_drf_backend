from rest_framework import serializers
from apps.questions.models import Question
from apps.api.serializers.answer_serializer import AnswerSerializer


class QuestionCreateSerializer(serializers.ModelSerializer[Question]):
    class Meta:
        model = Question
        fields = ['text']
    
    def validate_text(self, value: str) -> str:
        if not value or not value.strip():
            raise serializers.ValidationError("Текст вопроса не может быть пустым")
        return value.strip()
    

class QuestionDetailSerializer(serializers.ModelSerializer[Question]):
    answers = AnswerSerializer(many=True, read_only=True)
    answers_count = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at', 'answers', 'answers_count']

    def get_answers_count(self, obj: Question) -> int:
        return obj.answers.count()