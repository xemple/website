from django.contrib import admin
from apps.ftp.models import FTPUser, FTPDir


class FTPUserAdmin(admin.ModelAdmin):
	list_display = ('owner', 'login')

class FTPDirAdmin(admin.ModelAdmin):
	pass
	
	
admin.site.register(FTPUser, FTPUserAdmin)
admin.site.register(FTPDir, FTPDirAdmin)

