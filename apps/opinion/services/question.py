from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.opinion.models import Question
from apps.products.models import Product
from apps.users.models import User


class QuestionService:
    @staticmethod
    def get(question_uuid: str) -> Question:
        question = get_object_or_404(Question, uuid=question_uuid)
        return question

    @staticmethod
    def filter(product: Product) -> QuerySet[Question]:
        questions = Question.objects.filter(product=product)
        return questions

    @staticmethod
    def add_or_remove_likes(user: User, question: Question) -> None:
        if user in question.likes.all():
            question.likes.remove(user)
        else:
            question.likes.add(user)
            question.dislikes.remove(user)
