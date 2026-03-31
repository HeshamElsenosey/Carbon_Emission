from django.db import models

# Create your models here.
from django.conf import settings

class EmissionEntry(models.Model):
    #*    ربط العملية بالمستخدم (صاحب الشركة أو الحساب)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='emissions'
    )
    
    #*   تصنيف الانبعاثات (كهرباء، غاز، وقود، إلخ)
    CATEGORY_CHOICES = [
        ('electricity', 'الكهرباء'),
        ('natural_gas', 'الغاز الطبيعي'),
        ('petrol', 'بنزين السيارات'),
        ('diesel', 'ديزل (سولار)'),
        ('waste', 'النفايات'),
        ('hfc_134a', 'غاز تبريد HFC-134a'),
        ('hfc_410a', 'غاز تبريد HFC-410A'),
        ('r_22', 'غاز تبريد R-22'),
        ('steam', 'البخار المشتري / التدفئة'),
        ('flight', 'سفر بالطائرة'),
        ('car', 'سفر بالسيارة'),
        ('train', 'سفر بالقطار'),
        ('motorbike', 'سفر بالدراجة النارية'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    #*   القيمة التي يدخلها المستخدم (مثلاً 500)
    value = models.FloatField()
    
    #*   الوحدة (kWh, Liters, m3)
    unit = models.CharField(max_length=20)
    
    #*   النتيجة المحسوبة للكربون (kg CO2)
    carbon_footprint = models.FloatField(null=True, blank=True)
    
    #*  تاريخ تسجيل العملية
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.carbon_footprint} kg"