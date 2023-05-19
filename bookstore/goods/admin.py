from django.contrib import admin
from django.contrib.admin import site
from django.contrib.admin.views.main import *
from django.contrib.admin.widgets import AutocompleteSelectMultiple
from django.contrib.contenttypes.models import ContentType
from django.core.checks import Tags

from .models import (
    Item,
    Book,
    Figure,
    Tag,
    User,
    Profile
)


class ItemDetailModelAdmin(admin.ModelAdmin):
    fieldsets = None
    autocomplete_fields = ('tags', )

    def set_form_params(self, form, content_type):
        form.base_fields['content_type'].initial = content_type
        form.base_fields['content_type'].disabled = True
        form.base_fields['content_type'].widget.can_add_related = False
        form.base_fields['content_type'].widget.can_change_related = False

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(ItemDetailModelAdmin, self).get_form(request, obj, change, **kwargs)
        if hasattr(obj, 'content_type_id'):
            content_type = obj.content_type_id
        else:
            content_type = ContentType.objects.get(model=self.__class__.model.__name__.lower()).id
        self.set_form_params(form, content_type)
        return form

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     form_field = super().formfield_for_manytomany(db_field, request, **kwargs)
    #     if form_field:
    #         db = kwargs.get('using')
    #         if db_field.name == 'tags':
    #             form_field.widget = AutocompleteSelectMultiple(Tag._meta.get_field('tag_title'), site)
    #         if 'queryset' not in kwargs:
    #             queryset = self.get_field_queryset(db_field=db_field, request=request, db=db)
    #             print(queryset)
    #             if queryset is not None:
    #                 kwargs['queryset'] = queryset
    #         return form_field
    #     return form_field


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", 'price', "display_tags", "quantity")

    @admin.display(description='Tags')
    def display_tags(self, obj):
        return ', '.join([tag.tag_title for tag in obj.tags.all()])

    #
    # def get_form(self, request, obj=None, change=False, **kwargs):
    #     super().get_form(request, obj, change, **kwargs)
    # ct = obj.content_type.through.objects.filter(pk=obj.pk).values('content_type_id', 'model').first()
    # print(ct)


@admin.register(Book)
class BookAdminDetail(ItemDetailModelAdmin):
    model = Book
    list_display = ("id", "title", "quantity", "author")


@admin.register(Figure)
class FigureAdminDetail(ItemDetailModelAdmin):
    model = Figure
    list_display = ("id", "title", "quantity", "manufacturer")


@admin.action(description='Mark increase discount to 5')
def increase_discount(modeladmin, request, queryset):
    queryset.update(discount=F('discount') + 5)


@admin.action(description='Mark decrease discount to 5')
def decrease_discount(modeladmin, request, queryset):
    queryset.update(discount=F('discount') - 5)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_title', 'discount')
    actions = [increase_discount, decrease_discount]
    search_fields = ('tag_title', )
    ordering = ('pk', )

    def save_model(self, request, obj, form, change):
        if request.user.email == 'test@test.test':
            raise PermissionError('Нельзя!!!')

    def delete_model(self, request, obj):
        if request.user.email == 'test@test.test':
            raise PermissionError('Нельзя !!!')


# _____user_____

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "date_joined", "is_superuser")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "user_email", "user_first_name", "user_last_name", "balance")

    @admin.display(ordering='user__first_name')
    def user_first_name(self, obj):
        return obj.user.first_name

    @admin.display(ordering='user__last_name')
    def user_last_name(self, obj):
        return obj.user.last_name

    @admin.display(ordering='user__email')
    def user_email(self, obj):
        return obj.user.email
