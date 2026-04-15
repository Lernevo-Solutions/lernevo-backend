from django.contrib import admin
from .models import Role, Organization, User, WellnessType, UserProfile

admin.site.register(Role)
admin.site.register(Organization)
admin.site.register(User)
admin.site.register(WellnessType)
admin.site.register(UserProfile)