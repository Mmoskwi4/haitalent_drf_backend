import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from apps.questions.models import Question


@pytest.mark.django_db
class TestQuestionModel:
    """Тесты для модели Question с использованием pytest"""
    
    def test_create_question(self):
        """Тест создания вопроса"""
        question = Question.objects.create(text="Тестовый вопрос?")
        assert question.text == "Тестовый вопрос?"
        assert question.id is not None
    
    def test_question_string_representation(self):
        """Тест строкового представления"""
        question = Question.objects.create(text="Вопрос для теста?")
        assert str(question) == f"Question {question.id}"
    
    def test_question_verbose_names(self):
        """Тест verbose names"""
        assert Question._meta.verbose_name == "Вопрос"
        assert Question._meta.verbose_name_plural == "Вопросы"
    
    def test_question_table_name(self):
        """Тест имени таблицы"""
        assert Question._meta.db_table == "questions"


@pytest.mark.django_db
class TestQuestionAPI:
    """Тесты для API вопросов с использованием pytest"""
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def sample_question(self):
        return Question.objects.create(text="Тестовый вопрос для API?")
    
    def test_get_questions_list(self, api_client):
        """Тест получения списка вопросов"""
        # Создаем несколько вопросов для теста
        Question.objects.create(text="Первый вопрос?")
        Question.objects.create(text="Второй вопрос?")

        response = api_client.get(reverse('api:questions:question-list-create'))
        assert response.status_code == status.HTTP_200_OK
        
        # Для пагинированного ответа проверяем структуру
        assert 'results' in response.data
        assert isinstance(response.data['results'], list)
        assert len(response.data['results']) == 2
        assert response.data['count'] == 2
        assert response.data['next'] is None
        assert response.data['previous'] is None
    
        # Проверяем содержимое результатов
        questions_data = response.data['results']
        assert questions_data[0]['text'] == "Первый вопрос?"
        assert questions_data[1]['text'] == "Второй вопрос?"

    
    def test_create_question(self, api_client):
        """Тест создания вопроса через API"""
        data = {"text": "Новый вопрос через API?"}
        response = api_client.post(
            reverse('api:questions:question-list-create'),
            data,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == data['text']
        assert 'id' in response.data
    
    def test_create_question_empty_text(self, api_client):
        """Тест создания вопроса с пустым текстом"""
        data = {"text": ""}
        response = api_client.post(
            reverse('api:questions:question-list-create'),
            data,
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_get_question_detail(self, api_client, sample_question):
        """Тест получения деталей вопроса"""
        response = api_client.get(
            reverse('api:questions:question-detail', kwargs={'pk': sample_question.id})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == sample_question.id
        assert response.data['text'] == sample_question.text
    
    def test_delete_question(self, api_client, sample_question):
        """Тест удаления вопроса"""
        question_id = sample_question.id
        response = api_client.delete(
            reverse('api:questions:question-detail', kwargs={'pk': question_id})
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Question.objects.filter(id=question_id).exists()        