from django.views import generic
from braces.views import LoginRequiredMixin
from .models import Watch


class WatchesListView(LoginRequiredMixin, generic.ListView):
    queryset = Watch.objects.select_related('package')
    context_object_name = 'watches'
    template_name = 'watches/watches_list.html'

    def get_queryset(self):
        qs = super(WatchesListView, self).get_queryset()
        return qs.filter(user=self.request.user)

watches_list = WatchesListView.as_view()
