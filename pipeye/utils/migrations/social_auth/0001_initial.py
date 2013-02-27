# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserSocialAuth'
        db.create_table(u'social_auth_usersocialauth', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='social_auth', to=orm['accounts.User'])),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('extra_data', self.gf('social_auth.fields.JSONField')(default='{}')),
        ))
        db.send_create_signal('social_auth', ['UserSocialAuth'])

        # Adding unique constraint on 'UserSocialAuth', fields ['provider', 'uid']
        db.create_unique(u'social_auth_usersocialauth', ['provider', 'uid'])

        # Adding model 'Nonce'
        db.create_table(u'social_auth_nonce', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('timestamp', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('salt', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('social_auth', ['Nonce'])

        # Adding unique constraint on 'Nonce', fields ['server_url', 'timestamp', 'salt']
        db.create_unique(u'social_auth_nonce', ['server_url', 'timestamp', 'salt'])

        # Adding model 'Association'
        db.create_table(u'social_auth_association', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('handle', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('issued', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('lifetime', self.gf('django.db.models.fields.IntegerField')()),
            ('assoc_type', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('social_auth', ['Association'])

        # Adding unique constraint on 'Association', fields ['server_url', 'handle']
        db.create_unique(u'social_auth_association', ['server_url', 'handle'])


    def backwards(self, orm):
        # Removing unique constraint on 'Association', fields ['server_url', 'handle']
        db.delete_unique(u'social_auth_association', ['server_url', 'handle'])

        # Removing unique constraint on 'Nonce', fields ['server_url', 'timestamp', 'salt']
        db.delete_unique(u'social_auth_nonce', ['server_url', 'timestamp', 'salt'])

        # Removing unique constraint on 'UserSocialAuth', fields ['provider', 'uid']
        db.delete_unique(u'social_auth_usersocialauth', ['provider', 'uid'])

        # Deleting model 'UserSocialAuth'
        db.delete_table(u'social_auth_usersocialauth')

        # Deleting model 'Nonce'
        db.delete_table(u'social_auth_nonce')

        # Deleting model 'Association'
        db.delete_table(u'social_auth_association')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_mailout': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'preferred_mailout_time': ('django.db.models.fields.IntegerField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'})
        },
        'social_auth.association': {
            'Meta': {'unique_together': "(('server_url', 'handle'),)", 'object_name': 'Association'},
            'assoc_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'lifetime': ('django.db.models.fields.IntegerField', [], {}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'server_url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'social_auth.nonce': {
            'Meta': {'unique_together': "(('server_url', 'timestamp', 'salt'),)", 'object_name': 'Nonce'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'server_url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'social_auth.usersocialauth': {
            'Meta': {'unique_together': "(('provider', 'uid'),)", 'object_name': 'UserSocialAuth'},
            'extra_data': ('social_auth.fields.JSONField', [], {'default': "'{}'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'social_auth'", 'to': u"orm['accounts.User']"})
        }
    }

    complete_apps = ['social_auth']