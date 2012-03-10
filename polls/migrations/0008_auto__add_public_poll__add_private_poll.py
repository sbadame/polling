# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Public_Poll'
        db.create_table('polls_public_poll', (
            ('poll_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['polls.Poll'], unique=True, primary_key=True)),
            ('public_hash', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('polls', ['Public_Poll'])

        # Adding model 'Private_Poll'
        db.create_table('polls_private_poll', (
            ('poll_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['polls.Poll'], unique=True, primary_key=True)),
            ('private_hash', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('polls', ['Private_Poll'])


    def backwards(self, orm):
        
        # Deleting model 'Public_Poll'
        db.delete_table('polls_public_poll')

        # Deleting model 'Private_Poll'
        db.delete_table('polls_private_poll')


    models = {
        'polls.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {})
        },
        'polls.poll': {
            'Meta': {'object_name': 'Poll'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 10, 9, 9, 25, 678017)'}),
            'date_expire': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 3, 17, 9, 9, 25, 678048)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'total_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'polls.private_poll': {
            'Meta': {'object_name': 'Private_Poll', '_ormbases': ['polls.Poll']},
            'poll_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['polls.Poll']", 'unique': 'True', 'primary_key': 'True'}),
            'private_hash': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'polls.public_poll': {
            'Meta': {'object_name': 'Public_Poll', '_ormbases': ['polls.Poll']},
            'poll_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['polls.Poll']", 'unique': 'True', 'primary_key': 'True'}),
            'public_hash': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'polls.vote': {
            'Meta': {'object_name': 'Vote'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']"})
        }
    }

    complete_apps = ['polls']
