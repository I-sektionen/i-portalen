from django.contrib.auth.forms import UserChangeForm, UserCreationForm, ReadOnlyPasswordHashField
from django import forms
from .models import IUser, BachelorProfile, MasterProfile
from utils.validators import liu_id_validator

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
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
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


class ChangeUserInfoForm(forms.ModelForm):
    class Meta:
        model = IUser
        fields = ('address', 'zip_code', 'city', 'gender', 'allergies', 'start_year')


class AddWhiteListForm(forms.Form):
    users = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 15, "placeholder": "abcde123\nfghij456\nklmno789\n..."}),
        help_text="Ange ett liu-id per rad inga andra tecken är tillåtna."

    )

    def __init__(self, *args, **kwargs):
        super(AddWhiteListForm, self).__init__(*args, **kwargs)
        self.fields['users'].label = "Lista med Liu-id:n att lägga till:"


class MembershipForm(forms.Form):
    user = forms.CharField(label="Liu-id", validators=[liu_id_validator, ])
    password = forms.CharField(label='Lösenord', widget=forms.PasswordInput)


class SegmentUsersForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SegmentUsersForm, self).__init__(*args, **kwargs)
        self.fields['bachelor_profile'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                                    required=False,
                                                                    choices=[(o.pk, o.name) for o in BachelorProfile.objects.all()])

        self.fields['master_profile'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                                  required=False,
                                                                  choices=[(o.pk, o.name) for o in MasterProfile.objects.all()])

    gender = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                       choices=IUser.GENDER_OPTIONS,
                                       required=False)
    start_year = forms.IntegerField(min_value=1969,
                                    max_value=2500,
                                    required=False)
    current_year = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             choices=IUser.STUDY_YEARS,
                                             required=False)

    klass = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                      choices=IUser.CLASSES,
                                      required=False)

class SelectUserFieldsForm(forms.Form):
    FIELDS = (
        ('email', 'email'),
        ('first_name', 'förnamn'),
        ('last_name', 'efternamn'),
        ('gender', 'kön'),
        ('start_year', 'start år'),
        ('current_year', 'nuvarande årskurs'),
        ('bachelor_profile', 'teknisk inriktning'),
        ('master_profile', 'master profil'),
        ('city', 'stad'),
        ('zip_code', 'postnummer'),
        ('address', 'adress'),
        ('allergies', 'allergier'),
    )
    selected_fields = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                choices=FIELDS,
                                                required=False)