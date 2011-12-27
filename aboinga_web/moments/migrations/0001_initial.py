# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Moment'
        db.create_table('moments', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('upload_ip', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('moments', ['Moment'])


    def backwards(self, orm):
        
        # Deleting model 'Moment'
        db.delete_table('moments')


    models = {
        'moments.moment': {
            'Meta': {'object_name': 'Moment', 'db_table': "'moments'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'upload_ip': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['moments']
