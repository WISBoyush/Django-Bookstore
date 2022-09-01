from django.contrib import admin
from django.db.models import F

from .models import (
    Item,
    Book,
    Figure,
    Tag,
    User,
    Profile
)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", 'price', "display_tags", "quantity")

    @admin.display(description='Tags')
    def display_tags(self, obj):
        return ', '.join([tag.tag_title for tag in obj.tags.all()])


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "quantity", "author")


@admin.register(Figure)
class FigureAdmin(admin.ModelAdmin):
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
