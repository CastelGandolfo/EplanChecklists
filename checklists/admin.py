from django.contrib import admin

from .models import Project, Eplan, Device, ChecklistPoint, EplanDevice, SelectedCheckpoint


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, AuthorAdmin)
admin.site.register(Eplan, AuthorAdmin)
admin.site.register(EplanDevice, AuthorAdmin)
admin.site.register(Device, AuthorAdmin)
admin.site.register(ChecklistPoint, AuthorAdmin)
admin.site.register(SelectedCheckpoint, AuthorAdmin)
