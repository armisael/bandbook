# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Player'
        db.create_table('players_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(populate_from=('name', 'surname'), allow_duplicates=False, max_length=50, separator=u'-', blank=True, unique=True, overwrite=False, db_index=True)),
            ('instrument_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['instruments.InstrumentType'])),
        ))
        db.send_create_signal('players', ['Player'])


    def backwards(self, orm):
        
        # Deleting model 'Player'
        db.delete_table('players_player')


    models = {
        'instruments.instrumentcategory': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'InstrumentCategory'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'populate_from': "'name'", 'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'overwrite': 'False', 'db_index': 'True'})
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
        },
        'players.player': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Player'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instrument_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['instruments.InstrumentType']"}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'populate_from': "('name', 'surname')", 'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'overwrite': 'False', 'db_index': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['players']
