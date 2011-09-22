# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Action'
        db.create_table('actions_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('plugin', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('actions', ['Action'])

        # Adding model 'ActionParameter'
        db.create_table('actions_actionparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['actions.Action'])),
            ('name', self.gf('django.db.models.fields.SlugField')(max_length=255, db_index=True)),
            ('value', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='str', max_length=4)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('actions', ['ActionParameter'])

        # Adding unique constraint on 'ActionParameter', fields ['action', 'name']
        db.create_unique('actions_actionparameter', ['action_id', 'name'])

        # Adding model 'ActionLog'
        db.create_table('actions_actionlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('plugin', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parameters', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('args', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('kwargs', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('error', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('actions', ['ActionLog'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ActionParameter', fields ['action', 'name']
        db.delete_unique('actions_actionparameter', ['action_id', 'name'])

        # Deleting model 'Action'
        db.delete_table('actions_action')

        # Deleting model 'ActionParameter'
        db.delete_table('actions_actionparameter')

        # Deleting model 'ActionLog'
        db.delete_table('actions_actionlog')


    models = {
        'actions.action': {
            'Meta': {'ordering': "['name']", 'object_name': 'Action'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'actions.actionlog': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'ActionLog'},
            'args': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwargs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parameters': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'actions.actionparameter': {
            'Meta': {'ordering': "['action', 'name']", 'unique_together': "(['action', 'name'],)", 'object_name': 'ActionParameter'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['actions.Action']"}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'str'", 'max_length': '4'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['actions']
