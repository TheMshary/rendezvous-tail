from django.contrib import admin
from app.models import Event, Suggestion, Invite

# Register your models here.
admin.site.register(Event)
admin.site.register(Suggestion)
admin.site.register(Invite)
