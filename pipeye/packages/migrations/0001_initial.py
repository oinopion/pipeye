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
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='releases', to=orm['packages.Package'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('home_page', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('package_url', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('release_url', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('author', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('author_email', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('maintainer', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('maintainer_email', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
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
            'author': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'author_email': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'home_page': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maintainer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'maintainer_email': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'releases'", 'to': "orm['packages.Package']"}),
            'package_url': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'release_url': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['packages']