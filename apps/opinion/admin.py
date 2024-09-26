from django.contrib import admin
from django.utils.html import format_html

from apps.opinion.models import Opinion, Comment, Grades, Question


@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'advantages',
        'periods',
        'user_display',
        'product_display',
        'total_likes',
    )

    @admin.display(description='Пользователь')
    def user_display(self, obj: Opinion) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            obj.user.get_absolute_url(),
            obj.user,
        )

    @admin.display(description='Товар')
    def product_display(self, obj: Opinion) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            obj.product.get_absolute_url(),
            obj.product.name,
        )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'user_display',
        'opinion_display',
        'question_display',
        'total_likes',
    )

    @admin.display(description='Пользователь')
    def user_display(self, obj: Comment) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            obj.user.get_absolute_url(),
            obj.user,
        )

    @admin.display(description='Отзыв')
    def opinion_display(self, obj: Comment) -> str:
        return (
            format_html(
                '<a href="{}">{}</a>',
                obj.opinion.get_absolute_url(),
                obj.opinion,
            )
            if obj.opinion
            else None
        )

    @admin.display(description='Вопрос')
    def question_display(self, obj: Comment) -> str:
        return (
            format_html(
                '<a href="{}">{}</a>',
                obj.question.get_absolute_url(),
                obj.question,
            )
            if obj.question
            else None
        )


@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'title',
        'grade',
        'opinion_display',
    )

    @admin.display(description='Отзыв')
    def opinion_display(self, obj: Comment) -> str:
        return (
            format_html(
                '<a href="{}">{}</a>',
                obj.opinion.get_absolute_url(),
                obj.opinion,
            )
            if obj.opinion
            else None
        )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'title',
        'user_display',
        'product_display',
        'total_likes',
    )

    @admin.display(description='Пользователь')
    def user_display(self, obj: Question) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            obj.user.get_absolute_url(),
            obj.user,
        )

    @admin.display(description='Товар')
    def product_display(self, obj: Opinion) -> str:
        return format_html(
            '<a href="{}">{}</a>',
            obj.product.get_absolute_url(),
            obj.product.name,
        )
