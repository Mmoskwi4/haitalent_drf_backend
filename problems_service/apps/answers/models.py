from typing import Any
from django.db import models
import logging

logger = logging.getLogger(__name__)


class Answer(models.Model):
    question = models.ForeignKey(
        "questions.Question",
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name=("Вопрос"),
    )
    user_id = models.CharField(
        max_length=36, help_text="Идентификатор пользователя (UUID)"
    )
    text = models.TextField(max_length=2000, help_text="Текс ответа")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "answers"
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self) -> str:
        return f"Answer {self.id} to {self.question_id}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        is_new = self.pk is None
        result = super().save(*args, **kwargs)

        if is_new:
            logger.info(f"Created answer {self.id} for question {self.question_id}")
            return result
        else:
            logger.info(f"Updated answer {self.id} for question {self.question_id}")
            return result

    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]:
        answer_id = self.id
        question_id = self.question_id
        result = super().delete(*args, **kwargs)
        logger.info(f"Delete answer {answer_id} from question {question_id}")
        return result
