from rest_framework import serializers
from .models import User
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    #todo    نحدد أن كلمة المرور يجب أن تكون "للكتابة فقط" لزيادة الأمان
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # todo    هذه هي حقول (الاسم، الشركة، الهاتف، إلخ)
        fields = (
            'username', 'email', 'password', 'full_name', 
            'phone_number', 'company_name', 'company_address', 
            'employee_count', 'industry', 'is_organization'
        )

    def create(self, validated_data):
        # todo  هذه الدالة تقوم بإنشاء المستخدم وتشفير كلمة المرور تلقائياً
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            company_name=validated_data.get('company_name', ''),
            company_address=validated_data.get('company_address', ''),
            employee_count=validated_data.get('employee_count', 0),
            industry=validated_data.get('industry', ''),
            is_organization=validated_data.get('is_organization', False)
        )
        return user
    
# class ProfileSerializer(serializers.ModelSerializer):
#     username = serializers.ReadOnlyField(source='user.username') # لعرض الاسم مع الصورة

#     class Meta:
#         model = Profile
#         fields = ['username', 'image', 'bio']


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    # حقل الصورة سيعيد الرابط الكامل تلقائياً
    image = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'image', 'bio']