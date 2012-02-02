# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Poll'
        db.create_table('polls_poll', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('polls', ['Poll'])

        # Adding model 'Choice'
        db.create_table('polls_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Poll'])),
            ('choice', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('votes', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('polls', ['Choice'])

        # Adding model 'Vote'
        db.create_table('polls_vote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['polls.Poll'])),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('polls', ['Vote'])


    def backwards(self, orm):
        
        # Deleting model 'Poll'
        db.delete_table('polls_poll')

        # Deleting model 'Choice'
        db.delete_table('polls_choice')

        # Deleting model 'Vote'
        db.delete_table('polls_vote')


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
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'polls.vote': {
            'Meta': {'object_name': 'Vote'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['polls.Poll']"})
        }
    }

    complete_apps = ['polls']
