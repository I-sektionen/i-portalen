from django import forms

from fika_penalty.models import FikaPenalty


class FikaPenaltyForm(forms.ModelForm):
    class Meta:
        model = FikaPenalty
        exclude = ['date', 'organisation']

    def __init__(self, *args, **kwargs):
        org = None
        if "organisation" in kwargs:
            org = kwargs["organisation"]
            del kwargs["organisation"]
        super(FikaPenaltyForm, self).__init__(*args, **kwargs)
        user_list = org.organisationpost_set.all().values_list('user__id', 'user__username', 'user__first_name', 'user__last_name')

        choices = []
        for user in user_list:
            if user[2] and user[3]:
                choices.append((user[0], "{} {}".format(user[2].capitalize(), user[3].capitalize())))
            else:
                choices.append((user[0], user[1]))
        self.fields['user'].choices = choices
