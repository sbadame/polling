# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        db.rename_column('polls_poll', 'seen_ips', 'ips_seen')


    def backwards(self, orm):
        db.rename_column('polls_poll', 'ips_seen', 'seen_ips')


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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 20, 11, 6, 5, 309324)'}),
            'date_expire': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 27, 11, 6, 5, 309355)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ips_seen': ('django.db.models.fields.TextField', [], {}),
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
        'polls.randompollpick': {
            'Meta': {'object_name': 'RandomPollPick'},
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
