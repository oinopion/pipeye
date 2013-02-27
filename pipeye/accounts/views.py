from braces.views import LoginRequiredMixin
from django.views.generic import UpdateView
from .forms import UserPreferencesForm
from pipeye.utils.urls import url_lazy


class PreferencesView(LoginRequiredMixin, UpdateView):
    form_class = UserPreferencesForm
    template_name = 'accounts/preferences.html'
    success_url = url_lazy('preferences_view')

    def get_object(self, queryset=None):
        return self.request.user
preferences_view = PreferencesView.as_view()
