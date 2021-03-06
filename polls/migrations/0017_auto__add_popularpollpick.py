# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PopularPollPick'
        db.create_table('polls_popularpollpick', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Public_Poll'], unique=True)),
            ('index', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('polls', ['PopularPollPick'])


    def backwards(self, orm):
        
        # Deleting model 'PopularPollPick'
        db.delete_table('polls_popularpollpick')


    models = {
        'polls.choice': {
            'Meta': {'object_name': 'Choice'},
            'choice': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {})
        },
        'polls.mostvotedpollpick': {
            'Meta': {'object_name': 'MostVotedPollPick'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Public_Poll']", 'unique': 'True'})
        },
        'polls.newestpollpick': {
            'Meta': {'object_name': 'NewestPollPick'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Public_Poll']", 'unique': 'True'})
        },
        'polls.poll': {
            'Meta': {'object_name': 'Poll'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 4, 10, 32, 15, 22614)'}),
            'date_expire': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 11, 10, 32, 15, 22645)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ips_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ips_seen': ('django.db.models.fields.TextField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'total_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'polls.popularpollpick': {
            'Meta': {'object_name': 'PopularPollPick'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Public_Poll']", 'unique': 'True'})
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
