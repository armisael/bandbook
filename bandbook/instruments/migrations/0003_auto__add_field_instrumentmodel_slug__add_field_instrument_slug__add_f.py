# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'InstrumentModel.slug'
        db.add_column('instruments_instrumentmodel', 'slug', self.gf('django_extensions.db.fields.AutoSlugField')(default='', populate_from='name', allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, overwrite=False, db_index=True), keep_default=False)

        # Adding field 'Instrument.slug'
        db.add_column('instruments_instrument', 'slug', self.gf('django_extensions.db.fields.AutoSlugField')(default='', populate_from='code', allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, overwrite=False, db_index=True), keep_default=False)

        # Adding field 'InstrumentManufacturer.slug'
        db.add_column('instruments_instrumentmanufacturer', 'slug', self.gf('django_extensions.db.fields.AutoSlugField')(default='', populate_from='name', allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, overwrite=False, db_index=True), keep_default=False)

        # Adding field 'InstrumentType.slug'
        db.add_column('instruments_instrumenttype', 'slug', self.gf('django_extensions.db.fields.AutoSlugField')(default='', populate_from='name', allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, overwrite=False, db_index=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'InstrumentModel.slug'
        db.delete_column('instruments_instrumentmodel', 'slug')

        # Deleting field 'Instrument.slug'
        db.delete_column('instruments_instrument', 'slug')

        # Deleting field 'InstrumentManufacturer.slug'
        db.delete_column('instruments_instrumentmanufacturer', 'slug')

        # Deleting field 'InstrumentType.slug'
        db.delete_column('instruments_instrumenttype', 'slug')


    models = {
        'instruments.instrument': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Instrument'},
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
        'instruments.instrumentmanufacturer': {
            'Meta': {'ordering': "['name']", 'object_name': 'InstrumentManufacturer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'populate_from': "'name'", 'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'overwrite': 'False', 'db_index': 'True'})
        },
        'instruments.instrumentmodel': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'InstrumentModel'},
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
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'populate_from': "'name'", 'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'overwrite': 'False', 'db_index': 'True'})
        }
    }

    complete_apps = ['instruments']
