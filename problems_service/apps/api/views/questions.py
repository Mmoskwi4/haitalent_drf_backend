from django.db.models import QuerySet
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from django.db import transaction
from drf_spectacular.utils import extend_schema, extend_schema_view
import logging
from typing import Any, Type

from apps.questions.models import Question
from apps.api.serializers import question_serializer as q_ser

logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        summary="Получить список всех вопросов",
        description="Возвращает список всех вопросов с количеством ответов",
        tags=["Questions"],
    ),
    post=extend_schema(
        summary="Создать новый вопрос",
        description="Создает новый вопрос. Текст вопроса обязателен.",
        tags=["Questions"],
    ),
)
class QuestionListCreateView(generics.ListCreateAPIView[Question]):
    def get_serializer_class(
        self,
    ) -> Type[q_ser.QuestionCreateSerializer | q_ser.QuestionDetailSerializer]:
        if self.request.method == "POST":
            return q_ser.QuestionCreateSerializer
        return q_ser.QuestionDetailSerializer

    def get_queryset(self) -> QuerySet[Question]:
        return Question.objects.prefetch_related("answers").all()

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """GET /questions/ - список всех вопросов"""
        response = super().list(request, *args, **kwargs)
        logger.info("Retrieved list of questions")
        return response

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """POST /questions/ - создать новый вопрос"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            question = serializer.save()

        logger.info(f"Question created successfully: {question.id}")
        return Response(
            q_ser.QuestionDetailSerializer(question).data,
            status=status.HTTP_201_CREATED,
        )


@extend_schema_view(
    get=extend_schema(
        summary="Получить вопрос и ответы",
        description="Возвращает вопрос со всеми ответами на него",
        tags=["Questions"],
    ),
    delete=extend_schema(
        summary="Удалить вопрос",
        description="Удаляет вопрос и все связанные с ним ответы (каскадно)",
        tags=["Questions"],
    ),
)
class QuestionDetailView(generics.RetrieveDestroyAPIView[Question]):
    queryset = Question.objects.prefetch_related("answers")
    serializer_class = q_ser.QuestionDetailSerializer

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """GET /questions/{id} - получить вопрос и все ответы на него"""
        question = self.get_object()
        logger.info(f"Retrieved question {question.id} with answers")
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """DELETE /questions/{id} - удалить вопрос (вместе с ответами)"""
        question = self.get_object()
        question_id = question.id
        self.perform_destroy(question)
        logger.info(f"Question {question_id} deleted successfully with all its answers")
        return Response(status=status.HTTP_204_NO_CONTENT)
