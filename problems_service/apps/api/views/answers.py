from typing import Any
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from django.shortcuts import get_object_or_404
from django.db import transaction
from drf_spectacular.utils import extend_schema, extend_schema_view
import logging

from apps.questions.models import Question
from apps.answers.models import Answer
from apps.api.serializers import answer_serializer as a_ser

logger = logging.getLogger(__name__)

@extend_schema_view(
    post=extend_schema(
        summary='Добавить ответ к вопросу',
        description='Создает новый ответ для указанного вопроса',
        tags=['Answers'],
    )
)
class AnswerCreateView(generics.CreateAPIView[Answer]):
    queryset = Answer.objects.all()
    serializer_class = a_ser.AnswerCreateSerialier

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        question_id = kwargs.get('question_id')
        
        question = get_object_or_404(Question, id=question_id)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            answer = Answer.objects.create(
                question=question,
                user_id=serializer.validated_data['user_id'],
                text=serializer.validated_data['text']
            )
        
        logger.info(f"Answer {answer.id} created for question {question_id}")
        return Response(
            a_ser.AnswerSerializer(answer).data,
            status=status.HTTP_201_CREATED
        )

@extend_schema_view(
    get=extend_schema(
        summary='Получить ответ',
        description='Возвращает информацию о конкретном ответе',
        tags=['Answers'],
    ),
    delete=extend_schema(
        summary='Удалить ответ',
        description='Удаляет конкретный ответ',
        tags=['Answers'],
    )
)
class AnswerDetailView(generics.RetrieveDestroyAPIView[Answer]):
    queryset = Answer.objects.select_related('question')
    serializer_class = a_ser.AnswerSerializer

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        answer = self.get_object()
        logger.info(f"Retrieved answer {answer.id}")
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        answer = self.get_object()
        answer_id = answer.id
        self.perform_destroy(answer)
        logger.info(f"Answer {answer_id} deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)