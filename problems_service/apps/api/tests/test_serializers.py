import pytest
import uuid
from rest_framework.exceptions import ValidationError

from apps.api.serializers.answer_serializer import AnswerCreateSerialier, AnswerSerializer
from apps.api.serializers.question_serializer import QuestionCreateSerializer, QuestionListSerializer, QuestionDetailSerializer
from apps.questions.models import Question
from apps.answers.models import Answer


@pytest.mark.django_db
class TestAnswerSerializers:
    """Тесты для сериализаторов ответов"""

    def test_answer_create_serializer_valid_data(self):
        """Тест AnswerCreateSerialier с валидными данными"""
        data = {
            "user_id": "user_123",  # Простой строковый ID (не UUID)
            "text": "Валидный текст ответа"
        }
        serializer = AnswerCreateSerialier(data=data)
        assert serializer.is_valid()
        # validated_data доступен только после is_valid()
        assert serializer.validated_data['user_id'] == "user_123"
        assert serializer.validated_data['text'] == "Валидный текст ответа"
    
    def test_answer_create_serializer_valid_uuid(self):
        """Тест AnswerCreateSerialier с валидным UUID"""
        data = {
            "user_id": "550e8400-e29b-41d4-a716-446655440000",  # Валидный UUID
            "text": "Валидный текст ответа"
        }
        serializer = AnswerCreateSerialier(data=data)
        assert serializer.is_valid()
        # Проверяем что данные прошли валидацию
        assert 'user_id' in serializer.validated_data
        assert 'text' in serializer.validated_data
    
    def test_answer_create_serializer_invalid_user_id(self):
        """Тест AnswerCreateSerialier с невалидным user_id"""
        # Слишком длинный user_id
        data = {
            "user_id": "a" * 37,  # Превышает max_length=36
            "text": "Валидный текст"
        }
        serializer = AnswerCreateSerialier(data=data)
        assert not serializer.is_valid()
        assert 'user_id' in serializer.errors
        error_message = str(serializer.errors['user_id'][0])
        assert "36" in error_message or "max_length" in str(serializer.errors['user_id'])
    
    def test_answer_create_serializer_empty_user_id(self):
        """Тест AnswerCreateSerialier с пустым user_id"""
        data = {
            "user_id": "",
            "text": "Валидный текст"
        }
        serializer = AnswerCreateSerialier(data=data)
        assert not serializer.is_valid()
        assert 'user_id' in serializer.errors
    
    def test_answer_create_serializer_empty_text(self):
        """Тест AnswerCreateSerialier с пустым текстом"""
        data = {
            "user_id": "user_123",
            "text": ""
        }
        serializer = AnswerCreateSerialier(data=data)
        assert not serializer.is_valid()
        assert 'text' in serializer.errors
    
    def test_answer_serializer_fields(self):
        """Тест AnswerSerializer - проверка полей"""
        # Создаем mock-объект ответа
        class MockAnswer:
            id = 1
            question_id = 1
            user_id = "user_123"
            text = "Текст ответа"
            created_at = "2023-01-01T00:00:00Z"
            
            @property
            def question(self):
                class MockQuestion:
                    id = 1
                return MockQuestion()
        
        answer = MockAnswer()
        serializer = AnswerSerializer(answer)
        
        expected_fields = ['id', 'question_id', 'user_id', 'text', 'created_at']
        assert all(field in serializer.data for field in expected_fields)
        assert serializer.data['question_id'] == 1


@pytest.mark.django_db
class TestQuestionSerializers:
    """Тесты для сериализаторов вопросов"""
    
    def test_question_create_serializer_valid_data(self):
        """Тест QuestionCreateSerializer с валидными данными"""
        data = {"text": "Валидный текст вопроса?"}
        serializer = QuestionCreateSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data['text'] == "Валидный текст вопроса?"
    
    def test_question_create_serializer_empty_text(self):
        """Тест QuestionCreateSerializer с пустым текстом"""
        data = {"text": ""}
        serializer = QuestionCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert 'text' in serializer.errors
    
    def test_question_create_serializer_create_instance(self):
        """Тест создания экземпляра через QuestionCreateSerializer"""
        data = {"text": "Вопрос созданный через сериализатор?"}
        serializer = QuestionCreateSerializer(data=data)
        assert serializer.is_valid()
        
        question = serializer.save()
        assert question.id is not None
        assert question.text == data['text']
    
    def test_question_list_serializer(self):
        """Тест QuestionListSerializer"""
        question = Question.objects.create(text="Вопрос для списка?")
        # Создаем ответы для проверки счетчика
        Answer.objects.create(
            question=question,
            user_id="user_1",
            text="Первый ответ"
        )
        Answer.objects.create(
            question=question,
            user_id="user_2",
            text="Второй ответ"
        )
        
        serializer = QuestionListSerializer(question)
        data = serializer.data
        
        assert data['id'] == question.id
        assert data['text'] == question.text
        assert data['answers_count'] == 2
        assert 'created_at' in data
    
    def test_question_detail_serializer(self):
        """Тест QuestionDetailSerializer"""
        question = Question.objects.create(text="Вопрос для деталей?")
        answer = Answer.objects.create(
            question=question,
            user_id="detail_user",
            text="Ответ для детального просмотра"
        )
        
        serializer = QuestionDetailSerializer(question)
        data = serializer.data
        
        assert data['id'] == question.id
        assert data['text'] == question.text
        assert 'answers' in data
        assert len(data['answers']) == 1
        assert data['answers'][0]['id'] == answer.id
        assert data['answers_count'] == 1