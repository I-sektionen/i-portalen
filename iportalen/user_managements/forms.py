from django.contrib.auth.forms import UserChangeForm, UserCreationForm, ReadOnlyPasswordHashField
from django import forms
from .models import IUser

__author__ = 'jonathan'


class CustomUserCreationForm(UserCreationForm):
    """ A form for creating new users. Includes all the required fields, plus a repeated password. """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = IUser
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            IUser._default_manager.get(username=username)
        except IUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        #Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label="Lösenord",
        help_text="Ändra lösenordet med <a href=\'password/\'> det här formuläret</a>."
    )

    class Meta(UserChangeForm.Meta):
        model = IUser
        fields = ('username', 'password', 'is_active', 'is_staff', 'is_superuser', 'user_permissions')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]