from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from webapp.forms.user_forms import CreateUserForm, UpdateUserForm
from webapp.models.tweet import Tweet


class AdminUser(UserAdmin):
    add_form = CreateUserForm
    form = UpdateUserForm
    model = get_user_model()
    list_display = get_user_model().fields()


admin.site.register(get_user_model(), AdminUser)
admin.site.register(Tweet)
