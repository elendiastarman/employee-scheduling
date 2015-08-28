# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Address'
        db.delete_table('scheduler_address')

        # Deleting field 'Worker.address'
        db.delete_column('scheduler_worker', 'address_id')

        # Adding field 'Worker.street1'
        db.add_column('scheduler_worker', 'street1',
                      self.gf('django.db.models.fields.CharField')(max_length=200, default='', blank=True),
                      keep_default=False)

        # Adding field 'Worker.street2'
        db.add_column('scheduler_worker', 'street2',
                      self.gf('django.db.models.fields.CharField')(max_length=200, default='', blank=True),
                      keep_default=False)

        # Adding field 'Worker.city'
        db.add_column('scheduler_worker', 'city',
                      self.gf('django.db.models.fields.CharField')(max_length=200, default='', blank=True),
                      keep_default=False)

        # Adding field 'Worker.state'
        db.add_column('scheduler_worker', 'state',
                      self.gf('django.db.models.fields.CharField')(max_length=200, default='', blank=True),
                      keep_default=False)

        # Adding field 'Worker.zipcode'
        db.add_column('scheduler_worker', 'zipcode',
                      self.gf('django.db.models.fields.CharField')(max_length=10, default='', blank=True),
                      keep_default=False)

        # Adding field 'Worker.country'
        db.add_column('scheduler_worker', 'country',
                      self.gf('django.db.models.fields.CharField')(max_length=50, default='', blank=True),
                      keep_default=False)

        # Adding field 'Worker.time_updated'
        db.add_column('scheduler_worker', 'time_updated',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 10, 1, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'Worker.email'
        db.alter_column('scheduler_worker', 'email', self.gf('django.db.models.fields.EmailField')(max_length=200))

        # Changing field 'Worker.secondary_email'
        db.alter_column('scheduler_worker', 'secondary_email', self.gf('django.db.models.fields.EmailField')(max_length=200))

    def backwards(self, orm):
        # Adding model 'Address'
        db.create_table('scheduler_address', (
            ('street1', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('street2', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('time_updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('scheduler', ['Address'])

        # Adding field 'Worker.address'
        db.add_column('scheduler_worker', 'address',
                      self.gf('django.db.models.fields.related.ForeignKey')(null=True, default=None, to=orm['scheduler.Address']),
                      keep_default=False)

        # Deleting field 'Worker.street1'
        db.delete_column('scheduler_worker', 'street1')

        # Deleting field 'Worker.street2'
        db.delete_column('scheduler_worker', 'street2')

        # Deleting field 'Worker.city'
        db.delete_column('scheduler_worker', 'city')

        # Deleting field 'Worker.state'
        db.delete_column('scheduler_worker', 'state')

        # Deleting field 'Worker.zipcode'
        db.delete_column('scheduler_worker', 'zipcode')

        # Deleting field 'Worker.country'
        db.delete_column('scheduler_worker', 'country')

        # Deleting field 'Worker.time_updated'
        db.delete_column('scheduler_worker', 'time_updated')


        # Changing field 'Worker.email'
        db.alter_column('scheduler_worker', 'email', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Worker.secondary_email'
        db.alter_column('scheduler_worker', 'secondary_email', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
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
            'rank': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'SE'", 'unique': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        'scheduler.shift': {
            'Meta': {'object_name': 'Shift'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'default': 'None'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'default': 'None'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_worker': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'shift_originalWorker'", 'default': 'None', 'to': "orm['scheduler.Worker']", 'blank': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Position']"}),
            'sub_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'substitute_worker': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'shift_substituteWorker'", 'default': 'None', 'to': "orm['scheduler.Worker']", 'blank': 'True'}),
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
            'date_of_birth': ('django.db.models.fields.DateField', [], {'default': 'None', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            'has_a_car': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_international': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pay_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'rank': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scheduler.Rank']", 'blank': 'True'}),
            'secondary_email': ('django.db.models.fields.EmailField', [], {'max_length': '200', 'default': "''", 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'street1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'street2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'default': "''", 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'unique': 'True', 'to': "orm['auth.User']"}),
            'work_status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'default': "'AA'"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['scheduler']