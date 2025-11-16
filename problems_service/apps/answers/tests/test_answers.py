import pytest
import uuid
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from apps.questions.models import Question
from apps.answers.models import Answer


@pytest.mark.django_db
class TestAnswerModel:
    """Тесты для модели Answer с использованием pytest"""
    
    @pytest.fixture
    def sample_question(self):
        return Question.objects.create(text="Вопрос для ответов?")
    
    def test_create_answer(self, sample_question):
        """Тест создания ответа"""
        answer = Answer.objects.create(
            question=sample_question,
            user_id="test_user_123",
            text="Тестовый ответ"
        )
        assert answer.text == "Тестовый ответ"
        assert answer.user_id == "test_user_123"
        assert answer.question == sample_question
        assert answer.id is not None
    
    def test_answer_string_representation(self, sample_question):
        """Тест строкового представления"""
        answer = Answer.objects.create(
            question=sample_question,
            user_id="user_456",
            text="Ответ для теста"
        )
        assert str(answer) == f"Answer {answer.id} to {sample_question.id}"
    
    def test_answer_verbose_names(self):
        """Тест verbose names"""
        assert Answer._meta.verbose_name == "Ответ"
        assert Answer._meta.verbose_name_plural == "Ответы"
    
    def test_answer_relationship(self, sample_question):
        """Тест связи ответа с вопросом"""
        answer = Answer.objects.create(
            question=sample_question,
            user_id="user_789",
            text="Ответ для связи"
        )
        assert answer in sample_question.answers.all()
        assert sample_question.answers.count() == 1


@pytest.mark.django_db
class TestAnswerAPI:
    """Тесты для API ответов с использованием pytest"""
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def sample_question(self):
        return Question.objects.create(text="Вопрос для API тестов?")
    
    @pytest.fixture
    def sample_answer(self, sample_question):
        return Answer.objects.create(
            question=sample_question,
            user_id=str(uuid.uuid4()),
            text="Тестовый ответ для API"
        )
    
    def test_create_answer(self, api_client, sample_question):
        """Тест создания ответа через API"""
        data = {
            "user_id": "api_test_user",
            "text": "Ответ созданный через API"
        }
        response = api_client.post(
            reverse('api:answers:answer-create', kwargs={'question_id': sample_question.id}),
            data,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == data['text']
        assert response.data['question_id'] == sample_question.id
    
    def test_create_answer_with_uuid(self, api_client, sample_question):
        """Тест создания ответа с UUID"""
        data = {
            "user_id": str(uuid.uuid4()),
            "text": "Ответ с UUID пользователя"
        }
        response = api_client.post(
            reverse('api:answers:answer-create', kwargs={'question_id': sample_question.id}),
            data,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_create_answer_invalid_question(self, api_client):
        """Тест создания ответа для несуществующего вопроса"""
        data = {
            "user_id": "user_123",
            "text": "Ответ для несуществующего вопроса"
        }
        response = api_client.post(
            reverse('api:answers:answer-create', kwargs={'question_id': 999}),
            data,
            format='json'
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_answer_detail(self, api_client, sample_answer):
        """Тест получения деталей ответа"""
        response = api_client.get(
            reverse('api:answers:answer-detail', kwargs={'pk': sample_answer.id})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == sample_answer.id
        assert response.data['text'] == sample_answer.text
    
    def test_delete_answer(self, api_client, sample_answer):
        """Тест удаления ответа"""
        answer_id = sample_answer.id
        response = api_client.delete(
            reverse('api:answers:answer-detail', kwargs={'pk': answer_id})
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Answer.objects.filter(id=answer_id).exists()