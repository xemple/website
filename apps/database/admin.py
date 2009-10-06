from django.contrib import admin
from apps.database.models import Database, DatabaseServer, DatabaseUser


class DatabaseAdmin(admin.ModelAdmin):
	pass


class DatabaseServerAdmin(admin.ModelAdmin):
	pass
	
	
class DatabaseUserAdmin(admin.ModelAdmin):
	pass

admin.site.register(Database, DatabaseAdmin)
admin.site.register(DatabaseServer, DatabaseServerAdmin)
admin.site.register(DatabaseUser, DatabaseUserAdmin)
