from django.views import generic
from .models import Package


class PackageDetailView(generic.DetailView):
    model = Package
    slug_field = 'name'
    slug_url_kwarg = 'name'

package_detail = PackageDetailView.as_view()


class PackageSearchView(generic.ListView):
    allow_empty = True
    context_object_name = 'packages'
    queryset = Package.objects.order_by('name')
    template_name = 'packages/search.html'

    def get_queryset(self):
        if self.get_query():
            qs = super(PackageSearchView, self).get_queryset()
            return qs.filter(name__istartswith=self.get_query())
        else:
            return Package.objects.none()

    def get_query(self):
        return self.request.GET.get('q')

package_search = PackageSearchView.as_view()
