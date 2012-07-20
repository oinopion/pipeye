# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Package'
        db.create_table('packages_package', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
        ))
        db.send_create_signal('packages', ['Package'])

        # Adding model 'PackageRelease'
        db.create_table('packages_packagerelease', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['packages.Package'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('home_page', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('package_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('release_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('author', self.gf('django.db.models.fields.TextField')()),
            ('author_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('maintainer', self.gf('django.db.models.fields.TextField')()),
            ('maintainer_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('packages', ['PackageRelease'])

        # Adding unique constraint on 'PackageRelease', fields ['version', 'package']
        db.create_unique('packages_packagerelease', ['version', 'package_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PackageRelease', fields ['version', 'package']
        db.delete_unique('packages_packagerelease', ['version', 'package_id'])

        # Deleting model 'Package'
        db.delete_table('packages_package')

        # Deleting model 'PackageRelease'
        db.delete_table('packages_packagerelease')


    models = {
        'packages.package': {
            'Meta': {'object_name': 'Package'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'packages.packagerelease': {
            'Meta': {'unique_together': "(('version', 'package'),)", 'object_name': 'PackageRelease'},
            'author': ('django.db.models.fields.TextField', [], {}),
            'author_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'home_page': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maintainer': ('django.db.models.fields.TextField', [], {}),
            'maintainer_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['packages.Package']"}),
            'package_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'release_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['packages']