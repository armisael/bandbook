# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'InstrumentHistory'
        db.create_table('instruments_instrumenthistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('instrument', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instruments.Instrument'])),
            ('date_start', self.gf('django.db.models.fields.DateField')()),
            ('date_end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('event_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('instruments', ['InstrumentHistory'])


    def backwards(self, orm):
        
        # Deleting model 'InstrumentHistory'
        db.delete_table('instruments_instrumenthistory')


    models = {
        'instruments.instrument': {
            'Meta': {'ordering': "['model__type__ordering']", 'object_name': 'Instrument'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_of_purchase': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instruments.InstrumentModel']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'populate_from': "'code'", 'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'overwrite': 'False', 'db_index': 'True'})
        },
        'instruments.instrumentcategory': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'InstrumentCategory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'populate_from': "'name'", 'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'overwrite': 'False', 'db_index': 'True'})
        },
        'instruments.instrumenthistory': {
            'Meta': {'ordering': "['-date_start']", 'object_name': 'InstrumentHistory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'event_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instruments.Instrument']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'instruments.instrumentmanufacturer': {
            'Meta': {'ordering': "['name']", 'object_name': 'InstrumentManufacturer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'populate_from': "'name'", 'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'overwrite': 'False', 'db_index': 'True'})
        },
        'instruments.instrumentmodel': {
            'Meta': {'ordering': "['type__ordering']", 'object_name': 'InstrumentModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instruments.InstrumentManufacturer']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'populate_from': "'name'", 'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'overwrite': 'False', 'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instruments.InstrumentType']"})
        },
        'instruments.instrumenttype': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'InstrumentType'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instruments.InstrumentCategory']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '22'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'populate_from': "'name'", 'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'overwrite': 'False', 'db_index': 'True'})
        }
    }

    complete_apps = ['instruments']
