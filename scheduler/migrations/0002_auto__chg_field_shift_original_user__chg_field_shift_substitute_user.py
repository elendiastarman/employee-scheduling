# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Shift.original_user'
        db.alter_column('scheduler_shift', 'original_user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['scheduler.User']))

        # Changing field 'Shift.substitute_user'
        db.alter_column('scheduler_shift', 'substitute_user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['scheduler.User']))

    def backwards(self, orm):

        # Changing field 'Shift.original_user'
        db.alter_column('scheduler_shift', 'original_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.User'], default=None))

        # Changing field 'Shift.substitute_user'
        db.alter_column('scheduler_shift', 'substitute_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.User'], default=None))

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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.User']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'scheduler.position': {
            'Meta': {'object_name': 'Position'},
            'block': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'scheduler.rank': {
            'Meta': {'object_name': 'Rank'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'SE'"}),
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
            'original_user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['scheduler.User']", 'related_name': "'shift_originalUser'", 'default': 'None'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Position']"}),
            'substitute_user': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['scheduler.User']", 'related_name': "'shift_substituteUser'", 'default': 'None'}),
            'time_end': ('django.db.models.fields.TimeField', [], {}),
            'time_start': ('django.db.models.fields.TimeField', [], {}),
            'weekly': ('django.db.models.fields.BooleanField', [], {})
        },
        'scheduler.user': {
            'Meta': {'object_name': 'User'},
            'badge_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_currently_working': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Rank']"}),
            'secondary_email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'wage_rate': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'work_status': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['scheduler']