from django.test import TestCase
from expecter import expect
from ..forms import UserPreferencesForm


class UserPreferencesFormTest(TestCase):
    fields = ['username', 'email', 'preferred_mailout_time']

    def test_has_only_preferences_fields(self):
        form = UserPreferencesForm()
        expect(set(form.fields)) == set(self.fields)
