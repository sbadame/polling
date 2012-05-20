# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from pybloomfilter import BloomFilter

class Migration(DataMigration):

    def forwards(self, orm):
        for poll in orm.Poll.objects.all():
            poll.seen_ips = BloomFilter(1000, 0.01, '/tmp/test.bloom').to_base64()
            poll.save()


    def backwards(self, orm):
        "Write your backwards methods here."
        pass


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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 20, 9, 33, 23, 854248)'}),
            'date_expire': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 5, 27, 9, 33, 23, 854279)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'seen_ips': ('django.db.models.fields.TextField', [], {}),
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
