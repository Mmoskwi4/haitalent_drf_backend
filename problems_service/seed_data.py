import os
import django
import uuid

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'problems_service.settings')
django.setup()

from apps.questions.models import Question
from apps.answers.models import Answer

def main():
    """Заполнение базы данных тестовыми данными"""
    
    # Очистка существующих данных
    Answer.objects.all().delete()
    Question.objects.all().delete()
    
    print("Создание тестовых данных...")
    
    # Создание вопросов
    questions_data = [
        "Какой язык программирования лучше всего подходит для веб-разработки?",
        "Что такое ORM и зачем он нужен?",
        "В чем разница между REST и GraphQL?",
        "Как работает асинхронное программирование в Python?",
        "Какие базы данных лучше использовать для высоконагруженных приложений?",
        "Что такое контейнеризация и зачем нужен Docker?",
        "Как обеспечить безопасность веб-приложения?",
        "Какие фреймворки популярны для фронтенд-разработки в 2024?",
        "Что такое микросервисная архитектура?",
        "Как работает кэширование и какие инструменты использовать?",
        "Какие принципы SOLID вы знаете и как их применять?",
        "В чем преимущества использования TypeScript вместо JavaScript?",
        "Как настроить CI/CD для проекта?",
        "Что такое JWT и как он работает?",
        "Какие методы оптимизации производительности веб-приложений вы знаете?"
    ]
    
    questions = []
    for i, text in enumerate(questions_data):
        question = Question.objects.create(text=text)
        questions.append(question)
        print(f"Создан вопрос {i+1}: {text[:50]}...")
    
    # Создание ответов
    answers_data = [
        ("Python с Django/FastAPI отлично подходит для бэкенда", "user_1"),
        ("JavaScript/TypeScript с React/Vue для фронтенда", "user_2"),
        ("ORM - это прослойка между БД и кодом, упрощает работу", "dev_1"),
        ("REST использует HTTP методы, GraphQL - единую точку входа", "api_expert"),
        ("async/await в Python позволяет писать асинхронный код", "python_dev"),
        ("PostgreSQL для сложных данных, Redis для кэша", "db_admin"),
        ("Docker позволяет изолировать приложения в контейнерах", "devops_1"),
        ("Валидация входных данных, HTTPS, защита от XSS", "security_expert"),
        ("React, Vue.js, Angular, Svelte", "frontend_dev"),
        ("Микросервисы - это разбиение приложения на небольшие сервисы", "architect"),
        ("Redis, Memcached, CDN для статических файлов", "perf_engineer"),
        ("SOLID помогает писать поддерживаемый код", "senior_dev"),
        ("TypeScript добавляет типизацию, уменьшает ошибки", "ts_fan"),
        ("GitHub Actions, GitLab CI, Jenkins", "ci_cd_expert"),
        ("JWT - токены для аутентификации, содержат payload", "auth_specialist")
    ]
    
    for i, (answer_text, user_id) in enumerate(answers_data):
        question = questions[i % len(questions)]  # Распределяем ответы по вопросам
        Answer.objects.create(
            question=question,
            user_id=user_id,
            text=answer_text
        )
        print(f"Создан ответ {i+1} для вопроса {question.id}")
    
    # Добавим несколько ответов на один вопрос
    popular_question = questions[0]
    additional_answers = [
        ("JavaScript универсален и работает везде", "js_lover"),
        ("Go отлично подходит для высоконагруженных систем", "go_dev"),
        ("Ruby on Rails имеет отличную экосистему", "rails_fan")
    ]
    
    for text, user_id in additional_answers:
        Answer.objects.create(
            question=popular_question,
            user_id=user_id,
            text=text
        )
    
    print(f"\nСоздано {Question.objects.count()} вопросов и {Answer.objects.count()} ответов")
    print("Тестовые данные успешно добавлены!")

if __name__ == "__main__":
    main()