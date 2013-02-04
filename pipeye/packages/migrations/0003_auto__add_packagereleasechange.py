# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PackageReleaseChange'
        db.create_table('packages_packagereleasechange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changes', to=orm['packages.Package'])),
            ('release', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['packages.PackageRelease'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('packages', ['PackageReleaseChange'])


    def backwards(self, orm):
        # Deleting model 'PackageReleaseChange'
        db.delete_table('packages_packagereleasechange')


    models = {
        'packages.package': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Package'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_release': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['packages.PackageRelease']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'packages.packagerelease': {
            'Meta': {'ordering': "('-timestamp',)", 'unique_together': "(('version', 'package'),)", 'object_name': 'PackageRelease'},
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
        },
        'packages.packagereleasechange': {
            'Meta': {'object_name': 'PackageReleaseChange'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changes'", 'to': "orm['packages.Package']"}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['packages.PackageRelease']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        }
    }

    complete_apps = ['packages']