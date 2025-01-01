from django.contrib import admin
from .models import Register, OTP, Awards
# Register your models here.

admin.site.register(Register)
admin.site.register(Awards)
admin.site.register(OTP)
