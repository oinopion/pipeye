from django.core.urlresolvers import reverse
from django.views import generic
from braces.views import LoginRequiredMixin, UserFormKwargsMixin
from .models import Watch
from .forms import UserWatchForm


class WatchesListView(LoginRequiredMixin, generic.ListView):
    queryset = Watch.objects.select_related('package')
    context_object_name = 'watches'
    template_name = 'watches/watches_list.html'

    def get_queryset(self):
        qs = super(WatchesListView, self).get_queryset()
        return qs.filter(user=self.request.user)

watches_list = WatchesListView.as_view()


class CreateWatchView(LoginRequiredMixin, UserFormKwargsMixin, generic.CreateView):
    model = Watch
    template_name = 'watches/watch_form.html'
    form_class = UserWatchForm
    http_method_names = ['post']

    def get_success_url(self):
        return reverse('package_detail', args=[self.object.package.name])

create_watch = CreateWatchView.as_view()
