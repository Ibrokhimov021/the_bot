from dataclasses import field
from django.contrib import admin
from .models import Application, Facultet, Super, About
# Register your models here.



class ApplicationAdmin(admin.ModelAdmin):
    class Meta:
        model = Application
        fields = "__all__"


class AboutAdmin(admin.ModelAdmin):
    class Meta: 
        model = About
        fields = 'all'

class FacultetAdmin(admin.ModelAdmin):
    class Meta:
        model = Facultet
        fields='all'

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Facultet,FacultetAdmin)
admin.site.register(Super)
admin.site.register(About, AboutAdmin)