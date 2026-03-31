from rest_framework import serializers
from .models import EmissionEntry

class EmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionEntry
        fields = ['id', 'category', 'value', 'unit', 'carbon_footprint', 'date_created']
        # نجعل النتيجة للقراءة فقط لأن السيرفر هو من سيحسبها
        read_only_fields = ['carbon_footprint','date_created']

    # 1. التحقق من القيمة (Value Validation)
    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("عذراً، يجب أن تكون القيمة أكبر من الصفر. لا يمكن حساب انبعاثات لقيمة سالبة أو معدومة.")
        return value

    # 2. التحقق الشامل (Object-level Validation)
    def validate(self, data):
        category = data.get('category')
        unit = data.get('unit', '').lower()

        # التأكد من أن الوحدة مناسبة للتصنيف
        distance_categories = ['flight', 'car', 'train', 'motorbike']
        if category in distance_categories and unit not in ['km', 'mile', 'ميل', 'كيلومتر']:
            raise serializers.ValidationError(f"التصنيف {category} يتطلب وحدة قياس مسافة مثل (km) أو (mile).")

        if category == 'electricity' and unit not in ['kwh', 'megawatt', 'mw', 'mwh']:
            raise serializers.ValidationError("الكهرباء تتطلب وحدات طاقة مثل (kWh) أو (MW).")

        return data
    
#&---------------------------------------------------------------------------------------------------------------------------
    
    #* تعديل الوحدة فى حساب الإنبعاثات الكربونية للوقود
    def calculate_carbon(self, category, value, unit):
        unit = unit.lower()

        # 1. تحويلات الطاقة والتدفئة (Heating/Steam)
        if category == 'steam':
            if unit in ['mmbtu', 'مليون وحدة حرارية']:
                value = value * 293.07  # تحويل لـ kWh حراري
            elif unit in ['gj', 'gigajoule', 'جيجا جول']:
                value = value * 277.78  # تحويل لـ kWh حراري
        # تحويل النفايات (طن إلى كيلو جرام)
        elif category == 'waste' and unit in ['ton', 'طن', 't']:
            value = value * 1000  # الطن يساوي 1000 كيلو جرام   

        # 2. تحويلات الكهرباء (كما فعلنا سابقاً)
        elif category == 'electricity':
            if unit in ['megawatt', 'mw', 'mwh']:
                value = value * 1000

        # 3. تحويلات الوقود (جالون إلى لتر)
        elif unit in ['gallon', 'جالون']:
            value = value * 3.785

        # 4. تحويلات الغازات والنفايات (جرام إلى كيلو)
        elif unit in ['gram', 'جرام', 'gm']:
            value = value / 1000
        # 5. تحويل المسافات (Standardizing to KM)
        # إذا أدخل المستخدم المسافة بالميل (اختياري للإحترافية)
        elif unit in ['mile', 'ميل', 'mi']:
            value = value * 1.609
        
        # 2. معاملات الانبعاث للنقل (Scope 3 - Business Travel)
        # الأرقام تمثل kg CO2 لكل 1 كيلومتر مقطوع
        transport_factors = {
            'flight': 0.150,      # طائرة (متوسط للرحلات القصيرة/الطويلة)
            'car': 0.170,        # سيارة (متوسط استهلاك وقود)
            'train': 0.040,       # قطار (وسيلة صديقة للبيئة)
            'motorbike': 0.110,   # دراجة نارية
        }

        # 5. معاملات الانبعاث (Emission Factors)
        factors = {
            'electricity': 0.475,
            'steam': 0.200,      # معامل متوسط للبخار المشتري (kg CO2 per kWh)
            'natural_gas': 2.02,
            'petrol': 2.31,
            'diesel': 2.68,
            'hfc_134a': 1430,
            'hfc_410a': 2088,
            'r_22': 1810,
            'waste': 0.52,
            **transport_factors  # دمج معاملات النقل
        }
        
        factor = factors.get(category, 0)
        return value * factor


    def create(self, validated_data):
        # 1. جلب البيانات المدخلة
        category = validated_data.get('category')
        value = validated_data.get('value')
        unit = validated_data.get('unit')
        
        # 2. استدعاء دالة الحساب (التي تحتوي على تحويل الجالون والمعاملات)
        # تأكد أن دالة calculate_carbon موجودة في نفس الكلاس لديك
        validated_data['carbon_footprint'] = self.calculate_carbon(category, value, unit)
        
        # 3. ربط العملية بالمستخدم الذي قام بتسجيل الدخول حالياً
        validated_data['user'] = self.context['request'].user
        
        # 4. حفظ البيانات وإرجاع النتيجة (هذا السطر يكون آاااخر سطر في الدالة)
        return super().create(validated_data)