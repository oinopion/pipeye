from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from braces.views import LoginRequiredMixin
from pipeye.packages.models import Package
from .models import Watch


class WatchesListView(LoginRequiredMixin, generic.ListView):
    queryset = Watch.objects.select_related('package')
    context_object_name = 'watches'
    template_name = 'watches/watches_list.html'

    def get_queryset(self):
        qs = super(WatchesListView, self).get_queryset()
        return qs.filter(user=self.request.user)

watches_list = WatchesListView.as_view()


class CreateWatchView(LoginRequiredMixin, generic.View):
    def post(self, request, package_name):
        package = get_object_or_404(Package, name=package_name)
        Watch.objects.get_or_create(user=request.user, package=package)
        return redirect('package_detail', package.name)

create_watch = CreateWatchView.as_view()
