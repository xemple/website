from django.contrib import admin
from django.http import HttpResponse
from django.core import serializers




def export_as_xml(modeladmin, request, queryset):
    response = HttpResponse(mimetype="text/javascript")
    serializers.serialize("xml", queryset, stream=response)
    return response

admin.site.add_action(export_as_xml)