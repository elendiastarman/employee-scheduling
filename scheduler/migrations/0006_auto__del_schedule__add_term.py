# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Schedule'
        db.delete_table('scheduler_schedule')

        # Adding model 'Term'
        db.create_table('scheduler_term', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('descriptor', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('date_start', self.gf('django.db.models.fields.DateField')()),
            ('date_end', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('scheduler', ['Term'])


    def backwards(self, orm):
        # Adding model 'Schedule'
        db.create_table('scheduler_schedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('scheduler', ['Schedule'])

        # Deleting model 'Term'
        db.delete_table('scheduler_term')


    models = {
        'scheduler.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'street1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'street2': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'scheduler.position': {
            'Meta': {'object_name': 'Position'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'default_time_end': ('django.db.models.fields.TimeField', [], {}),
            'default_time_start': ('django.db.models.fields.TimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'scheduler.rank': {
            'Meta': {'object_name': 'Rank'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'SE'", 'max_length': '2'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        'scheduler.shift': {
            'Meta': {'object_name': 'Shift'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_worker': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'blank': 'True', 'null': 'True', 'to': "orm['scheduler.Worker']", 'related_name': "'shift_originalWorker'"}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Position']"}),
            'substitute_worker': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'blank': 'True', 'null': 'True', 'to': "orm['scheduler.Worker']", 'related_name': "'shift_substituteWorker'"}),
            'time_end': ('django.db.models.fields.TimeField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'time_start': ('django.db.models.fields.TimeField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'weekly': ('django.db.models.fields.BooleanField', [], {})
        },
        'scheduler.term': {
            'Meta': {'object_name': 'Term'},
            'date_end': ('django.db.models.fields.DateField', [], {}),
            'date_start': ('django.db.models.fields.DateField', [], {}),
            'descriptor': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scheduler.worker': {
            'Meta': {'object_name': 'Worker'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Address']"}),
            'badge_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pay_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Rank']"}),
            'secondary_email': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '200'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'work_status': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['scheduler']