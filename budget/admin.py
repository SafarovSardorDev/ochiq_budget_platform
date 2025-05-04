from django.contrib import admin
from .models import UserProfile, Project, Feedback, Reward, Check

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Feedback)
admin.site.register(Reward)
admin.site.register(Check)