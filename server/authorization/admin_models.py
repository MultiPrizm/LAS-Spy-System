from django.contrib import admin

class AddWorkStation(admin.ModelAdmin):
    list_display = ('name',)