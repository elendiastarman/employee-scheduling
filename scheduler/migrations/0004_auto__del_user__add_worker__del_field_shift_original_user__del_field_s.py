# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'User'
        db.delete_table('scheduler_user')

        # Adding model 'Worker'
        db.create_table('scheduler_worker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('secondary_email', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('badge_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.Address'])),
            ('pay_rate', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=5)),
            ('work_status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('rank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.Rank'])),
        ))
        db.send_create_signal('scheduler', ['Worker'])

        # Deleting field 'Shift.original_user'
        db.delete_column('scheduler_shift', 'original_user_id')

        # Deleting field 'Shift.substitute_user'
        db.delete_column('scheduler_shift', 'substitute_user_id')

        # Adding field 'Shift.original_worker'
        db.add_column('scheduler_shift', 'original_worker',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['scheduler.Worker'], blank=True, null=True, related_name='shift_originalWorker'),
                      keep_default=False)

        # Adding field 'Shift.substitute_worker'
        db.add_column('scheduler_shift', 'substitute_worker',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['scheduler.Worker'], blank=True, null=True, related_name='shift_substituteWorker'),
                      keep_default=False)

        # Deleting field 'Address.user'
        db.delete_column('scheduler_address', 'user_id')


    def backwards(self, orm):
        # Adding model 'User'
        db.create_table('scheduler_user', (
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rank', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.Rank'])),
            ('work_status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('pay_rate', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, max_digits=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('secondary_email', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('badge_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal('scheduler', ['User'])

        # Deleting model 'Worker'
        db.delete_table('scheduler_worker')

        # Adding field 'Shift.original_user'
        db.add_column('scheduler_shift', 'original_user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='shift_originalUser', to=orm['scheduler.User'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Shift.substitute_user'
        db.add_column('scheduler_shift', 'substitute_user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='shift_substituteUser', to=orm['scheduler.User'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Shift.original_worker'
        db.delete_column('scheduler_shift', 'original_worker_id')

        # Deleting field 'Shift.substitute_worker'
        db.delete_column('scheduler_shift', 'substitute_worker_id')


        # User chose to not deal with backwards NULL issues for 'Address.user'
        raise RuntimeError("Cannot reverse this migration. 'Address.user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Address.user'
        db.add_column('scheduler_address', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.User']),
                      keep_default=False)


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
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'scheduler.rank': {
            'Meta': {'object_name': 'Rank'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rank': ('django.db.models.fields.CharField', [], {'default': "'SE'", 'max_length': '2', 'unique': 'True'}),
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
            'original_worker': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['scheduler.Worker']", 'blank': 'True', 'null': 'True', 'related_name': "'shift_originalWorker'"}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Position']"}),
            'substitute_worker': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['scheduler.Worker']", 'blank': 'True', 'null': 'True', 'related_name': "'shift_substituteWorker'"}),
            'time_end': ('django.db.models.fields.TimeField', [], {}),
            'time_start': ('django.db.models.fields.TimeField', [], {}),
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
            'secondary_email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'work_status': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['scheduler']