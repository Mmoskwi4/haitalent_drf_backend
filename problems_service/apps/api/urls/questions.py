from django.urls import path
from apps.api.views import questions as q_views


app_name = "questions"

urlpatterns = [
    path('questions/', q_views.QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', q_views.QuestionDetailView.as_view(), name='question-detail'),
]