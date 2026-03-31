from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

#todo    تخصيص طريقة عرض المستخدم في لوحة الإدارة
class CustomUserAdmin(UserAdmin):
    #todo    الحقول التي ستظهر في قائمة المستخدمين
    list_display = ('username', 'email', 'full_name', 'company_name', 'is_staff')
    
    #todo    إضافة الحقول الجديدة داخل صفحة تعديل المستخدم
    fieldsets = UserAdmin.fieldsets + (
        ('معلومات إضافية', {'fields': ('full_name', 'phone_number', 'company_name', 'company_address', 'employee_count', 'industry', 'is_organization')}),
    )

#todo    تسجيل الموديل الجديد
admin.site.register(User, CustomUserAdmin)