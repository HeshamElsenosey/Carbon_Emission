from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        print("✅ تم تفعيل الـ Signals بنجاح يا هندسة!")
        # استخدام النقطة يعني "من المجلد الحالي"
        from . import signals




# from django.apps import AppConfig



# class UsersConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'users'  # تأكد أن هذا الاسم يطابق اسم مجلد التطبيق عندك

#     def ready(self):
#         # استدعاء ملف الـ signals عند جاهزية التطبيق
#         import users.signals
