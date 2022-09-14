from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = get_user_model()


class CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + tuple(get_user_model().fields())


class UpdateUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = get_user_model().update_fields()
