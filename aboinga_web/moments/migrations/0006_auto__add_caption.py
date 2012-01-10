# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Caption'
        db.create_table('captions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('moment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['moments.Moment'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('upload_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('moments', ['Caption'])


    def backwards(self, orm):
        
        # Deleting model 'Caption'
        db.delete_table('captions')


    models = {
        'moments.caption': {
            'Meta': {'object_name': 'Caption', 'db_table': "'captions'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['moments.Moment']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'upload_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'moments.flag': {
            'Meta': {'object_name': 'Flag', 'db_table': "'flags'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['moments.Moment']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'upload_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
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
            'upload_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'moments.rating': {
            'Meta': {'object_name': 'Rating', 'db_table': "'ratings'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['moments.Moment']"}),
            'stars': ('django.db.models.fields.SmallIntegerField', [], {}),
            'upload_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['moments']
