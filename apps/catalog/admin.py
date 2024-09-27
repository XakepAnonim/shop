from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from apps.catalog.models import Category


class CategoryInline(admin.StackedInline):
    """
    Инлайн для добавления подкатегорий прямо из страницы родительской категории.
    """

    model = Category
    extra = 1
    show_change_link = True
    fk_name = 'parent'
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    """
    Административный интерфейс для категории с поддержкой иерархии.
    """

    list_display = ('name', 'slug', 'uuid', 'parent')
    search_fields = ('name',)
    readonly_fields = ('uuid',)
    prepopulated_fields = {'slug': ('name',)}
    mptt_level_indent = 20

    inlines = [CategoryInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('products')
