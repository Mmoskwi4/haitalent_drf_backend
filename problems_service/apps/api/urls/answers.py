from django.urls import path
from apps.api.views import answers as a_views


app_name = "answers"

urlpatterns = [
    path('questions/<int:question_id>/answers/', a_views.AnswerCreateView.as_view(), name='answer-create'),
    path('answers/<int:pk>/', a_views.AnswerDetailView.as_view(), name='answer-detail'),
]