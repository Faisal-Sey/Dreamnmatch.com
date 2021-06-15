from django.contrib import admin
from .models import Profile, Qualities, Payment, MessageDetail, Messaging, Status, StatusImage

# Register your models here.
admin.site.register(Profile)
admin.site.register(Qualities)
admin.site.register(Messaging)
admin.site.register(Payment)
admin.site.register(MessageDetail)
admin.site.register(Status)
admin.site.register(StatusImage)