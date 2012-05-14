# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RandomPollList'
        db.create_table('polls_randompolllist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Public_Poll'], unique=True)),
            ('index', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('polls', ['RandomPollList'])

        # Changing field 'Public_Poll.public_hash'
        db.alter_column('polls_public_poll', 'public_hash', self.gf('django.db.models.fields.IntegerField')())


    def backwards(self, orm):
        
        # Deleting model 'RandomPollList'
        db.delete_table('polls_randompolllist')

        # Changing field 'Public_Poll.public_hash'
        db.alter_column('polls_public_poll', 'public_hash', self.gf('django.db.models.fields.CharField')(max_length=200))


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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 13, 20, 43, 33, 630117)'}),
            'date_expire': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 20, 20, 43, 33, 630148)'}),
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
            'public_hash': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'polls.randompolllist': {
            'Meta': {'object_name': 'RandomPollList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Public_Poll']", 'unique': 'True'})
        },
        'polls.vote': {
            'Meta': {'object_name': 'Vote'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']"})
        }
    }

    complete_apps = ['polls']
