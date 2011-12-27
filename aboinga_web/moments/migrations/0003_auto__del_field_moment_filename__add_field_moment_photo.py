# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Moment.filename'
        db.delete_column('moments', 'filename')

        # Adding field 'Moment.photo'
        db.add_column('moments', 'photo', self.gf('django.db.models.fields.files.FileField')(default='', max_length=100), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Moment.filename'
        db.add_column('moments', 'filename', self.gf('django.db.models.fields.CharField')(default='', max_length=255, unique=True, db_index=True), keep_default=False)

        # Deleting field 'Moment.photo'
        db.delete_column('moments', 'photo')


    models = {
        'moments.moment': {
            'Meta': {'object_name': 'Moment', 'db_table': "'moments'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'upload_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['moments']
