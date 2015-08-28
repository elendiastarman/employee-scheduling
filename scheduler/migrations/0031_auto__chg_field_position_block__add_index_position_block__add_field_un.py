# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Position.block' to match new field type.
        db.rename_column('scheduler_position', 'block', 'block_id')
        # Changing field 'Position.block'
        db.alter_column('scheduler_position', 'block_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['scheduler.Block']))
        # Adding index on 'Position', fields ['block']
        db.create_index('scheduler_position', ['block_id'])

        # Adding field 'Unit.weekdays'
        db.add_column('scheduler_unit', 'weekdays',
                      self.gf('django.db.models.fields.CharField')(max_length=8, default='MTWRF'),
                      keep_default=False)


    def backwards(self, orm):
        # Removing index on 'Position', fields ['block']
        db.delete_index('scheduler_position', ['block_id'])


        # User chose to not deal with backwards NULL issues for 'Position.block'
        raise RuntimeError("Cannot reverse this migration. 'Position.block' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Renaming column for 'Position.block' to match new field type.
        db.rename_column('scheduler_position', 'block_id', 'block')
        # Changing field 'Position.block'
        db.alter_column('scheduler_position', 'block', self.gf('django.db.models.fields.CharField')(max_length=1))
        # Deleting field 'Unit.weekdays'
        db.delete_column('scheduler_unit', 'weekdays')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scheduler.announcement': {
            'Meta': {'object_name': 'Announcement'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_to_delete': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 12, 15, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200', 'blank': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '3', 'default': "'3An'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Unit']"})
        },
        'scheduler.block': {
            'Meta': {'object_name': 'Block'},
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Unit']"})
        },
        'scheduler.position': {
            'Meta': {'object_name': 'Position'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'default': 'None', 'null': 'True', 'to': "orm['scheduler.Block']"}),
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
        'scheduler.record': {
            'Meta': {'object_name': 'Record'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'I'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'time_edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Worker']"})
        },
        'scheduler.shift': {
            'Meta': {'object_name': 'Shift'},
            'chain_nex': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'default': 'None', 'related_name': "'chain_bef'", 'null': 'True', 'to': "orm['scheduler.Shift']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_end': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_worker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'default': 'None', 'related_name': "'shift_originalWorker'", 'null': 'True', 'to': "orm['scheduler.Worker']"}),
            'pick_requests': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'pick_requests'", 'to': "orm['scheduler.Worker']"}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Position']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'O'"}),
            'sub_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sub_weeks': ('django.db.models.fields.CharField', [], {'max_length': '200', 'default': "''"}),
            'substitute_worker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'default': 'None', 'related_name': "'shift_substituteWorker'", 'null': 'True', 'to': "orm['scheduler.Worker']"}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['scheduler.Term']"}),
            'time_end': ('django.db.models.fields.TimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'time_start': ('django.db.models.fields.TimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['scheduler.Unit']"}),
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
            'hourly_limit': ('django.db.models.fields.IntegerField', [], {'default': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sub_request_in_advance': ('django.db.models.fields.IntegerField', [], {'default': '72'}),
            'weekdays': ('django.db.models.fields.CharField', [], {'max_length': '8', 'default': "'MTWRF'"})
        },
        'scheduler.unitstatus': {
            'Meta': {'object_name': 'UnitStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Unit']"}),
            'work_status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'AA'"}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Worker']"})
        },
        'scheduler.worker': {
            'Meta': {'object_name': 'Worker'},
            'approval_status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'NA'"}),
            'availability': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'badge_number': ('django.db.models.fields.CharField', [], {'max_length': '8', 'default': "''", 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'has_a_car': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hourly_limit': ('django.db.models.fields.IntegerField', [], {'default': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pay_rate': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': '0', 'max_digits': '5'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['scheduler.Rank']"}),
            'secondary_email': ('django.db.models.fields.EmailField', [], {'max_length': '200', 'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'street_1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'street_2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'default': "''", 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True'}),
            'tshirt_size': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['scheduler']