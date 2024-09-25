from django.contrib import admin
from django.utils.html import format_html

from apps.opinion.models import Opinion, Comment, Grades, Question


@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'user_display',
        'product',
        'total_likes',
    )

    @admin.display(description='Пользователь')
    def user_display(self, obj: Opinion) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            obj.user.get_absolute_url(),
            obj.user,
        )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'user_display',
        'opinion',
        'total_likes',
    )

    @admin.display(description='Пользователь')
    def user_display(self, obj: Comment) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            obj.user.get_absolute_url(),
            obj.user,
        )


@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'title',
        'grade',
        'opinion',
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'user_display',
        'product',
        'total_likes',
    )

    @admin.display(description='Пользователь')
    def user_display(self, obj: Question) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            obj.user.get_absolute_url(),
            obj.user,
        )
