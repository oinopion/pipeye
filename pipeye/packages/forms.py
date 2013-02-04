from django import forms
from .models import Package, PackageRelease


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['name']


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
