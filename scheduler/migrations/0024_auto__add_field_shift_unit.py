# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Shift.unit'
        db.add_column('scheduler_shift', 'unit',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scheduler.Unit'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Shift.unit'
        db.delete_column('scheduler_shift', 'unit_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scheduler.announcement': {
            'Meta': {'object_name': 'Announcement'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_to_destroy': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 11, 2, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'blank': 'True', 'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            'rank': ('django.db.models.fields.CharField', [], {'default': "'SE'", 'max_length': '2', 'unique': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        'scheduler.record': {
            'Meta': {'object_name': 'Record'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'time_edited': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Worker']"})
        },
        'scheduler.shift': {
            'Meta': {'object_name': 'Shift'},
            'chain_nex': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['scheduler.Shift']", 'default': 'None', 'null': 'True', 'related_name': "'chain_bef'", 'unique': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_end': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_worker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'default': 'None', 'null': 'True', 'related_name': "'shift_originalWorker'", 'to': "orm['scheduler.Worker']"}),
            'pick_requests': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['scheduler.Worker']", 'symmetrical': 'False', 'related_name': "'pick_requests'"}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Position']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'O'", 'max_length': '2'}),
            'sub_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sub_weeks': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'substitute_worker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'default': 'None', 'null': 'True', 'related_name': "'shift_substituteWorker'", 'to': "orm['scheduler.Worker']"}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Term']", 'null': 'True'}),
            'time_end': ('django.db.models.fields.TimeField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'time_start': ('django.db.models.fields.TimeField', [], {'blank': 'True', 'default': 'None', 'null': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Unit']", 'null': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sub_request_in_advance': ('django.db.models.fields.IntegerField', [], {'default': '72'})
        },
        'scheduler.unitstatus': {
            'Meta': {'object_name': 'UnitStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Unit']"}),
            'work_status': ('django.db.models.fields.CharField', [], {'default': "'AA'", 'max_length': '2'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Worker']"})
        },
        'scheduler.worker': {
            'Meta': {'object_name': 'Worker'},
            'approval_status': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '2'}),
            'availability': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'badge_number': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '8'}),
            'city': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'country': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'has_a_car': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pay_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'default': '0', 'decimal_places': '2'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Rank']", 'null': 'True'}),
            'secondary_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'default': "''", 'max_length': '200'}),
            'state': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'street_1': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'street_2': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'telephone': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '15'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True', 'auto_now_add': 'True'}),
            'tshirt_size': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '2'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'null': 'True', 'unique': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '10'})
        }
    }

    complete_apps = ['scheduler']