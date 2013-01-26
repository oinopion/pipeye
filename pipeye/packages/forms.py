from django import forms
from .models import PackageRelease


class PackageReleaseForm(forms.ModelForm):
    class Meta:
        model = PackageRelease
        fields = [
            'version',
            'summary',
            'home_page',
            'package_url',
            'release_url',
            'author',
            'author_email',
            'maintainer',
            'maintainer_email',
        ]
