# -*- coding: utf-8 -*-
 
from south.db import db
from django.db import models
from apps.service.models import *
 
class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'VZTemplate'
        db.create_table('service_vztemplate', (
            ('id', orm['service.VZTemplate:id']),
            ('filename', orm['service.VZTemplate:filename']),
            ('name', orm['service.VZTemplate:name']),
            ('version', orm['service.VZTemplate:version']),
            ('is_active', orm['service.VZTemplate:is_active']),
            ('created_at', orm['service.VZTemplate:created_at']),
            ('edited_at', orm['service.VZTemplate:edited_at']),
        ))
        db.send_create_signal('service', ['VZTemplate'])
        
        # Adding model 'SiteTechnology'
        db.create_table('service_sitetechnology', (
            ('id', orm['service.SiteTechnology:id']),
            ('is_specific', orm['service.SiteTechnology:is_specific']),
            ('type', orm['service.SiteTechnology:type']),
            ('revision', orm['service.SiteTechnology:revision']),
            ('beta', orm['service.SiteTechnology:beta']),
            ('autoupdate', orm['service.SiteTechnology:autoupdate']),
            ('created_at', orm['service.SiteTechnology:created_at']),
            ('edited_at', orm['service.SiteTechnology:edited_at']),
        ))
        db.send_create_signal('service', ['SiteTechnology'])
        
        # Adding model 'Service'
        db.create_table('service_service', (
            ('id', orm['service.Service:id']),
            ('client', orm['service.Service:client']),
            ('name', orm['service.Service:name']),
            ('created_at', orm['service.Service:created_at']),
            ('edited_at', orm['service.Service:edited_at']),
        ))
        db.send_create_signal('service', ['Service'])
        
        # Adding model 'Site'
        db.create_table('service_site', (
            ('id', orm['service.Site:id']),
            ('domain', orm['service.Site:domain']),
            ('technology', orm['service.Site:technology']),
            ('name', orm['service.Site:name']),
            ('created_at', orm['service.Site:created_at']),
            ('edited_at', orm['service.Site:edited_at']),
        ))
        db.send_create_signal('service', ['Site'])
        
        # Adding model 'DomainService'
        db.create_table('service_domainservice', (
            ('service_ptr', orm['service.DomainService:service_ptr']),
            ('domain', orm['service.DomainService:domain']),
        ))
        db.send_create_signal('service', ['DomainService'])
        
        # Adding model 'HostingService'
        db.create_table('service_hostingservice', (
            ('service_ptr', orm['service.HostingService:service_ptr']),
            ('ip', orm['service.HostingService:ip']),
            ('root', orm['service.HostingService:root']),
            ('template', orm['service.HostingService:template']),
        ))
        db.send_create_signal('service', ['HostingService'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'VZTemplate'
        db.delete_table('service_vztemplate')
        
        # Deleting model 'SiteTechnology'
        db.delete_table('service_sitetechnology')
        
        # Deleting model 'Service'
        db.delete_table('service_service')
        
        # Deleting model 'Site'
        db.delete_table('service_site')
        
        # Deleting model 'DomainService'
        db.delete_table('service_domainservice')
        
        # Deleting model 'HostingService'
        db.delete_table('service_hostingservice')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'client.client': {
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'service.domainservice': {
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['service.Service']", 'unique': 'True', 'primary_key': 'True'})
        },
        'service.hostingservice': {
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'root': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'service_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['service.Service']", 'unique': 'True', 'primary_key': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'service.service': {
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'service'", 'to': "orm['client.Client']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'edited_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'service.site': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attached_site'", 'to': "orm['service.Service']"}),
            'edited_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'technology': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'used_on_site'", 'to': "orm['service.SiteTechnology']"})
        },
        'service.sitetechnology': {
            'autoupdate': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'beta': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'edited_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_specific': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'service.vztemplate': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'edited_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'filename': ('django.db.models.fields.FilePathField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }
    
    complete_apps = ['service']