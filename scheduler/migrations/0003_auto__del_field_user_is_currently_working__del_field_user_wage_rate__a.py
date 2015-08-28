# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'User.is_currently_working'
        db.delete_column('scheduler_user', 'is_currently_working')

        # Deleting field 'User.wage_rate'
        db.delete_column('scheduler_user', 'wage_rate')

        # Adding field 'User.pay_rate'
        db.add_column('scheduler_user', 'pay_rate',
                      self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=5, default=0),
                      keep_default=False)


        # Changing field 'User.work_status'
        db.alter_column('scheduler_user', 'work_status', self.gf('django.db.models.fields.CharField')(max_length=2))
        # Adding unique constraint on 'Rank', fields ['rank']
        db.create_unique('scheduler_rank', ['rank'])


    def backwards(self, orm):
        # Removing unique constraint on 'Rank', fields ['rank']
        db.delete_unique('scheduler_rank', ['rank'])

        # Adding field 'User.is_currently_working'
        db.add_column('scheduler_user', 'is_currently_working',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'User.wage_rate'
        raise RuntimeError("Cannot reverse this migration. 'User.wage_rate' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'User.wage_rate'
        db.add_column('scheduler_user', 'wage_rate',
                      self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=5),
                      keep_default=False)

        # Deleting field 'User.pay_rate'
        db.delete_column('scheduler_user', 'pay_rate')


        # Changing field 'User.work_status'
        db.alter_column('scheduler_user', 'work_status', self.gf('django.db.models.fields.CharField')(max_length=100))

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
            'rank': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'SE'", 'max_length': '2'}),
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
            'original_user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['scheduler.User']", 'null': 'True', 'blank': 'True', 'related_name': "'shift_originalUser'"}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Position']"}),
            'substitute_user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['scheduler.User']", 'null': 'True', 'blank': 'True', 'related_name': "'shift_substituteUser'"}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pay_rate': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'max_digits': '5'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Rank']"}),
            'secondary_email': ('django.db.models.fields.CharField', [], {'default': "''", 'blank': 'True', 'max_length': '200'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'work_status': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['scheduler']