from django.shortcuts import get_object_or_404

from apps.opinion.models import OpinionComment
from apps.users.models import User


class OpinionCommentService:
    @staticmethod
    def get(opinion_uuid: str) -> OpinionComment:
        opinion_comment = get_object_or_404(OpinionComment, uuid=opinion_uuid)
        return opinion_comment

    @staticmethod
    def add_or_remove_likes(
        user: User, opinion_comment: OpinionComment
    ) -> None:
        if user in opinion_comment.likes.all():
            opinion_comment.likes.remove(user)
        else:
            opinion_comment.likes.add(user)
            opinion_comment.dislikes.remove(user)
