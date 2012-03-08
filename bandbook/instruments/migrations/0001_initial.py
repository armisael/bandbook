# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'InstrumentCategory'
        db.create_table('instruments_instrumentcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('instruments', ['InstrumentCategory'])

        # Adding model 'InstrumentType'
        db.create_table('instruments_instrumenttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instruments.InstrumentCategory'])),
            ('ordering', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('instruments', ['InstrumentType'])

        # Adding model 'InstrumentManufacturer'
        db.create_table('instruments_instrumentmanufacturer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('instruments', ['InstrumentManufacturer'])

        # Adding model 'InstrumentModel'
        db.create_table('instruments_instrumentmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instruments.InstrumentType'])),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instruments.InstrumentManufacturer'])),
        ))
        db.send_create_signal('instruments', ['InstrumentModel'])

        # Adding model 'Instrument'
        db.create_table('instruments_instrument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instruments.InstrumentModel'])),
            ('date_of_purchase', self.gf('django.db.models.fields.DateField')()),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('instruments', ['Instrument'])


    def backwards(self, orm):
        
        # Deleting model 'InstrumentCategory'
        db.delete_table('instruments_instrumentcategory')

        # Deleting model 'InstrumentType'
        db.delete_table('instruments_instrumenttype')

        # Deleting model 'InstrumentManufacturer'
        db.delete_table('instruments_instrumentmanufacturer')

        # Deleting model 'InstrumentModel'
        db.delete_table('instruments_instrumentmodel')

        # Deleting model 'Instrument'
        db.delete_table('instruments_instrument')


    models = {
        'instruments.instrument': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Instrument'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_of_purchase': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instruments.InstrumentModel']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
        'instruments.instrumentcategory': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'InstrumentCategory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {})
        },
        'instruments.instrumentmanufacturer': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'InstrumentManufacturer'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'instruments.instrumentmodel': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'InstrumentModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instruments.InstrumentManufacturer']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instruments.InstrumentType']"})
        },
        'instruments.instrumenttype': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'InstrumentType'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instruments.InstrumentCategory']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['instruments']
