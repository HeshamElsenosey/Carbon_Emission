from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.


class User(AbstractUser):
    #todo   1. المعلومات الشخصية فى صفحة التسجيل 

    full_name = models.CharField(max_length=255, verbose_name="الاسم الكامل")
    phone_number = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    
    #todo   2. معلومات الشركة فى صفحة التسجيل (اختيارية)
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="اسم المنشأة")
    company_address = models.CharField(max_length=500, blank=True, null=True, verbose_name="عنوان الشركة")
    employee_count = models.IntegerField(default=0, verbose_name="عدد الموظفين")
    industry = models.CharField(max_length=100, blank=True, null=True, verbose_name="المجال/الصناعة")
    
    #todo   3. إعدادات الحساب
    is_organization = models.BooleanField(default=False, verbose_name="هل هو حساب مؤسسة؟")

    def __str__(self):
        return f"{self.username} - {self.company_name if self.company_name else 'Individual'}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'

    # دالة الحفظ المعدلة لضغط الصورة
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)