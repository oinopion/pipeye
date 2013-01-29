from django import forms
from .models import Watch


class UserWatchForm(forms.ModelForm):
    class Meta:
        model = Watch
        fields = ('package', )

    def __init__(self, **kwargs):
        self.user = kwargs.pop('user')
        super(UserWatchForm, self).__init__(**kwargs)

    def save(self, commit=True):
        self.instance.user = self.user
        return super(UserWatchForm, self).save(commit=commit)
