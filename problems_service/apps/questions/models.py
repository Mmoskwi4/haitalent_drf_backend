from typing import Any
from django.db import models
import logging


logger = logging.getLogger(__name__)

class Question(models.Model):
    text = models.TextField(
        max_length=1000,
        help_text="Текст вопроса"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'questions'
        ordering = ['id']
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self) -> str:
        return f"Question {self.id}"
    
    def save(self, *args: Any, **kwargs: Any) -> None:
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"Created question {self.id}")
        else:
            logger.info(f"Updated question {self.id}")

    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]:
        question_id = self.id
        result = super().delete(*args, **kwargs)
        logger.info(f"Deleted question {question_id} with all its answers")
        return result