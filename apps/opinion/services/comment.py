from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.opinion.models import Comment, Opinion, Question
from apps.users.models import User


class CommentService:
    """
    Сервис для работы с комментариями
    """

    @staticmethod
    def filter_opinion(opinion: Opinion) -> QuerySet[Comment]:
        """
        Фильтрация комментариев по отзыву
        """
        opinion_comments = Comment.objects.filter(opinion=opinion)
        return opinion_comments

    @staticmethod
    def filter_question(question: Question) -> QuerySet[Comment]:
        """
        Фильтрация комментариев по вопросу
        """
        question_comments = Comment.objects.filter(question=question)
        return question_comments

    @staticmethod
    def add_or_remove_likes(user: User, opinion_comment: Comment) -> None:
        """
        Добавление или удаление лайков комментариям
        """
        if user in opinion_comment.likes.all():
            opinion_comment.likes.remove(user)
        else:
            opinion_comment.likes.add(user)
            opinion_comment.dislikes.remove(user)

    @staticmethod
    def add_or_remove_dislikes(user: User, opinion_comment: Comment) -> None:
        """
        Добавление или удаление дизлайков комментариям
        """
        if user in opinion_comment.dislikes.all():
            opinion_comment.dislikes.remove(user)
        else:
            opinion_comment.dislikes.add(user)
            opinion_comment.likes.remove(user)
