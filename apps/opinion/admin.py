from django.contrib import admin
from django.utils.html import format_html

from apps.opinion.models import Opinion, OpinionComment, Grades


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


@admin.register(OpinionComment)
class OpinionCommentAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'user_display',
        'opinion',
        'total_likes',
    )

    @admin.display(description='Пользователь')
    def user_display(self, obj: OpinionComment) -> str:
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
