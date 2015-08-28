# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field pick_requests on 'Shift'
        m2m_table_name = db.shorten_name('scheduler_shift_pick_requests')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('shift', models.ForeignKey(orm['scheduler.shift'], null=False)),
            ('worker', models.ForeignKey(orm['scheduler.worker'], null=False))
        ))
        db.create_unique(m2m_table_name, ['shift_id', 'worker_id'])


    def backwards(self, orm):
        # Removing M2M table for field pick_requests on 'Shift'
        db.delete_table(db.shorten_name('scheduler_shift_pick_requests'))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scheduler.announcement': {
            'Meta': {'object_name': 'Announcement'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_to_destroy': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 10, 10, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200', 'blank': 'True'}),
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
            'rank': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2', 'default': "'SE'"}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        'scheduler.record': {
            'Meta': {'object_name': 'Record'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'I'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'time_added': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_edited': ('django.db.models.fields.TimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Worker']"})
        },
        'scheduler.shift': {
            'Meta': {'object_name': 'Shift'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'default': 'None'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'default': 'None'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_worker': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['scheduler.Worker']", 'default': 'None', 'blank': 'True', 'related_name': "'shift_originalWorker'"}),
            'pick_requests': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['scheduler.Worker']", 'symmetrical': 'False'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Position']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'O'"}),
            'sub_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sub_weeks': ('django.db.models.fields.CharField', [], {'max_length': '200', 'default': "''"}),
            'substitute_worker': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['scheduler.Worker']", 'default': 'None', 'blank': 'True', 'related_name': "'shift_substituteWorker'"}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['scheduler.Term']"}),
            'time_end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
            'time_start': ('django.db.models.fields.TimeField', [], {'null': 'True', 'default': 'None', 'blank': 'True'}),
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
            'badge_number': ('django.db.models.fields.CharField', [], {'max_length': '8', 'default': "''", 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'has_a_car': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pay_rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'decimal_places': '2', 'max_digits': '5'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['scheduler.Rank']"}),
            'secondary_email': ('django.db.models.fields.EmailField', [], {'max_length': '200', 'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'street_1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'street_2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'default': "''", 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'tshirt_size': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'work_status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'AA'"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['scheduler']