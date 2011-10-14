# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):
	depends_on = (
		( "mailinglists", "0003_auto__del_mailchimpsourcelist__del_unique_mailchimpsourcelist_mailchim.py" ),
	)

	def forwards(self, orm):
		"Write your forwards methods here."
		for a in orm.Action.objects.filter( plugin__startswith='djangoplicity.mailinglists.tasks.actions.' ):
			a.plugin = a.plugin.replace( 'djangoplicity.mailinglists.tasks.actions.', 'djangoplicity.mailinglists.tasks.mailman_actions.' )
			a.save()


	def backwards(self, orm):
		"Write your backwards methods here."
		for a in orm.Action.objects.filter( plugin__startswith='djangoplicity.mailinglists.tasks.mailman_actions.' ):
			a.plugin = a.plugin.replace( 'djangoplicity.mailinglists.tasks.mailman_actions.', 'djangoplicity.mailinglists.tasks.actions.' )
			a.save()


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
