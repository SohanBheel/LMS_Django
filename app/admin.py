from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register((UserProfile,Enrollment,Notification,Feedback,Forum_post,Material,StudentUpdate))
