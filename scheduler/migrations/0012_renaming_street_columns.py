# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
##        # Deleting field 'Worker.street2'
##        db.delete_column('scheduler_worker', 'street2')
##
##        # Deleting field 'Worker.street1'
##        db.delete_column('scheduler_worker', 'street1')
##
##        # Adding field 'Worker.street_1'
##        db.add_column('scheduler_worker', 'street_1',
##                      self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=200),
##                      keep_default=False)
##
##        # Adding field 'Worker.street_2'
##        db.add_column('scheduler_worker', 'street_2',
##                      self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=200),
##                      keep_default=False)
        db.rename_column('scheduler_worker', 'street1', 'street_1')
        db.rename_column('scheduler_worker', 'street2', 'street_2')

        # Changing field 'Worker.time_updated'
        db.alter_column('scheduler_worker', 'time_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True))

    def backwards(self, orm):
##        # Adding field 'Worker.street2'
##        db.add_column('scheduler_worker', 'street2',
##                      self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=200),
##                      keep_default=False)
##
##        # Adding field 'Worker.street1'
##        db.add_column('scheduler_worker', 'street1',
##                      self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=200),
##                      keep_default=False)
##
##        # Deleting field 'Worker.street_1'
##        db.delete_column('scheduler_worker', 'street_1')
##
##        # Deleting field 'Worker.street_2'
##        db.delete_column('scheduler_worker', 'street_2')
        db.rename_column('scheduler_worker', 'street_1', 'street1')
        db.rename_column('scheduler_worker', 'street_2', 'street2')


        # Changing field 'Worker.time_updated'
        db.alter_column('scheduler_worker', 'time_updated', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'date_end': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_worker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'default': 'None', 'related_name': "'shift_originalWorker'", 'to': "orm['scheduler.Worker']", 'null': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Position']"}),
            'sub_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'substitute_worker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'default': 'None', 'related_name': "'shift_substituteWorker'", 'to': "orm['scheduler.Worker']", 'null': 'True'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Term']", 'null': 'True'}),
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
        'scheduler.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scheduler.worker': {
            'Meta': {'object_name': 'Worker'},
            'badge_number': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '8'}),
            'city': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'country': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'has_a_car': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pay_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2', 'default': '0'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Rank']", 'null': 'True'}),
            'secondary_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'default': "''", 'max_length': '200'}),
            'state': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'street_1': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'street_2': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'telephone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '15'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'to': "orm['auth.User']", 'unique': 'True'}),
            'work_status': ('django.db.models.fields.CharField', [], {'default': "'AA'", 'max_length': '2'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '10'})
        }
    }

    complete_apps = ['scheduler']
