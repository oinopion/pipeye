from braces.views import LoginRequiredMixin
from django.views.generic import UpdateView
from .forms import UserPreferencesForm
from pipeye.utils.urls import url_lazy


class PreferencesView(LoginRequiredMixin, UpdateView):
    form_class = UserPreferencesForm
    template_name = 'accounts/preferences.html'
    success_url = url_lazy('preferences')

    def get_object(self, queryset=None):
        return self.request.user
preferences = PreferencesView.as_view()
