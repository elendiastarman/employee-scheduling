# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Position.default_time_start'
        db.add_column('scheduler_position', 'default_time_start',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.time(13, 30)),
                      keep_default=False)

        # Adding field 'Position.default_time_end'
        db.add_column('scheduler_position', 'default_time_end',
                      self.gf('django.db.models.fields.TimeField')(default=datetime.time(16, 30)),
                      keep_default=False)


        # Changing field 'Shift.time_end'
        db.alter_column('scheduler_shift', 'time_end', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Shift.time_start'
        db.alter_column('scheduler_shift', 'time_start', self.gf('django.db.models.fields.TimeField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Position.default_time_start'
        db.delete_column('scheduler_position', 'default_time_start')

        # Deleting field 'Position.default_time_end'
        db.delete_column('scheduler_position', 'default_time_end')


        # User chose to not deal with backwards NULL issues for 'Shift.time_end'
        raise RuntimeError("Cannot reverse this migration. 'Shift.time_end' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Shift.time_end'
        db.alter_column('scheduler_shift', 'time_end', self.gf('django.db.models.fields.TimeField')())

        # User chose to not deal with backwards NULL issues for 'Shift.time_start'
        raise RuntimeError("Cannot reverse this migration. 'Shift.time_start' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Shift.time_start'
        db.alter_column('scheduler_shift', 'time_start', self.gf('django.db.models.fields.TimeField')())

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
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'SE'", 'unique': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        'scheduler.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'scheduler.shift': {
            'Meta': {'object_name': 'Shift'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_worker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'shift_originalWorker'", 'null': 'True', 'default': 'None', 'to': "orm['scheduler.Worker']"}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Position']"}),
            'substitute_worker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'shift_substituteWorker'", 'null': 'True', 'default': 'None', 'to': "orm['scheduler.Worker']"}),
            'time_end': ('django.db.models.fields.TimeField', [], {'blank': 'True', 'null': 'True', 'default': 'None'}),
            'time_start': ('django.db.models.fields.TimeField', [], {'blank': 'True', 'null': 'True', 'default': 'None'}),
            'weekly': ('django.db.models.fields.BooleanField', [], {})
        },
        'scheduler.worker': {
            'Meta': {'object_name': 'Worker'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Address']"}),
            'badge_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pay_rate': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Rank']"}),
            'secondary_email': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200', 'default': "''"}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'work_status': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['scheduler']