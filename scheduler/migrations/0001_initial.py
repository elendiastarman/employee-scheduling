# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table('scheduler_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('secondary_email', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('badge_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('wage_rate', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=5)),
            ('work_status', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_currently_working', self.gf('django.db.models.fields.BooleanField')()),
            ('rank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.Rank'])),
        ))
        db.send_create_signal('scheduler', ['User'])

        # Adding model 'Shift'
        db.create_table('scheduler_shift', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shift_originalUser', default=None, to=orm['scheduler.User'])),
            ('substitute_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shift_substituteUser', default=None, to=orm['scheduler.User'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time_start', self.gf('django.db.models.fields.TimeField')()),
            ('time_end', self.gf('django.db.models.fields.TimeField')()),
            ('weekly', self.gf('django.db.models.fields.BooleanField')()),
            ('position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.Position'])),
        ))
        db.send_create_signal('scheduler', ['Shift'])

        # Adding model 'Position'
        db.create_table('scheduler_position', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('block', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('scheduler', ['Position'])

        # Adding model 'Rank'
        db.create_table('scheduler_rank', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rank', self.gf('django.db.models.fields.CharField')(max_length=2, default='SE')),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('time_updated', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('scheduler', ['Rank'])

        # Adding model 'Address'
        db.create_table('scheduler_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.User'])),
            ('street1', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('street2', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('time_updated', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('scheduler', ['Address'])

        # Adding model 'Schedule'
        db.create_table('scheduler_schedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('scheduler', ['Schedule'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table('scheduler_user')

        # Deleting model 'Shift'
        db.delete_table('scheduler_shift')

        # Deleting model 'Position'
        db.delete_table('scheduler_position')

        # Deleting model 'Rank'
        db.delete_table('scheduler_rank')

        # Deleting model 'Address'
        db.delete_table('scheduler_address')

        # Deleting model 'Schedule'
        db.delete_table('scheduler_schedule')


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
            'original_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shift_originalUser'", 'default': 'None', 'to': "orm['scheduler.User']"}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Position']"}),
            'substitute_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shift_substituteUser'", 'default': 'None', 'to': "orm['scheduler.User']"}),
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