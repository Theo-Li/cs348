from django.contrib import admin
from .models import Student, Club, Room, Meeting, MeetingOrganizer

admin.site.register(Student)
admin.site.register(Club)
admin.site.register(Room)
admin.site.register(Meeting)
admin.site.register(MeetingOrganizer)
