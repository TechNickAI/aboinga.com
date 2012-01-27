# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'Rating', fields ['upload_ip']
        db.create_index('ratings', ['upload_ip'])

        # Adding index on 'Caption', fields ['upload_ip']
        db.create_index('captions', ['upload_ip'])

        # Adding index on 'Flag', fields ['upload_ip']
        db.create_index('flags', ['upload_ip'])

        # Adding index on 'Moment', fields ['upload_ip']
        db.create_index('moments', ['upload_ip'])


    def backwards(self, orm):
        
        # Removing index on 'Moment', fields ['upload_ip']
        db.delete_index('moments', ['upload_ip'])

        # Removing index on 'Flag', fields ['upload_ip']
        db.delete_index('flags', ['upload_ip'])

        # Removing index on 'Caption', fields ['upload_ip']
        db.delete_index('captions', ['upload_ip'])

        # Removing index on 'Rating', fields ['upload_ip']
        db.delete_index('ratings', ['upload_ip'])


    models = {
        'moments.caption': {
            'Meta': {'object_name': 'Caption', 'db_table': "'captions'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['moments.Moment']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'upload_ip': ('django.db.models.fields.IPAddressField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'moments.flag': {
            'Meta': {'object_name': 'Flag', 'db_table': "'flags'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['moments.Moment']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'upload_ip': ('django.db.models.fields.IPAddressField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'moments.moment': {
            'Meta': {'object_name': 'Moment', 'db_table': "'moments'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'photo_md5': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'upload_ip': ('django.db.models.fields.IPAddressField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'moments.rating': {
            'Meta': {'object_name': 'Rating', 'db_table': "'ratings'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['moments.Moment']"}),
            'stars': ('django.db.models.fields.SmallIntegerField', [], {}),
            'upload_ip': ('django.db.models.fields.IPAddressField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['moments']
