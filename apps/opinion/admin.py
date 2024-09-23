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

    def user_display(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            obj.user.get_absolute_url(),
            obj.user,
        )

    user_display.short_description = 'Пользователь'


@admin.register(OpinionComment)
class OpinionCommentAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'user_display',
        'opinion',
        'total_likes',
    )

    def user_display(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            obj.user.get_absolute_url(),
            obj.user,
        )

    user_display.short_description = 'Пользователь'


@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'title',
        'grade',
        'opinion',
    )
