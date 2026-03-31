from django.shortcuts import render
from django.utils import timezone
# Create your views here.
from rest_framework import generics, permissions
from .models import EmissionEntry
from .serializers import EmissionSerializer
#إعداد التقارير
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import EmissionEntry
from .serializers import EmissionSerializer

class EmissionListCreateView(generics.ListCreateAPIView):
    serializer_class = EmissionSerializer
    # يجب أن يكون المستخدم مسجل دخول (Login) لكي يصل لهذا الرابط
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # المستخدم يرى فقط العمليات الخاصة بشركته/حسابه الشخصي
        return EmissionEntry.objects.filter(user=self.request.user)

    # --- أضف هذه الدالة هنا لدعم الإدخال المتعدد ---
    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        
        # حفظ البيانات مع ربطها بالمستخدم
        if is_many:
            for item in serializer.validated_data:
                item['user'] = request.user
            serializer.save()
        else:
            serializer.save(user=request.user)
            
        return Response(serializer.data, status=201)
    # ---------------------------------------------
    # def perform_create(self, serializer):
    #     # نمرر المستخدم الحالي للـ Serializer أثناء الحفظ
    #     serializer.save(user=self.request.user)


#dashboard view
# from django.db.models import Sum
# from rest_framework.views import APIView
# from rest_framework.response import Response

class EmissionDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_emissions = EmissionEntry.objects.filter(user=request.user)
        
        # جمع إجمالي الكربون لكل التصنيفات
        total_carbon = user_emissions.aggregate(Sum('carbon_footprint'))['carbon_footprint__sum'] or 0
        
        # جمع التفاصيل حسب النوع (كهرباء، وقود، إلخ)
        by_category = user_emissions.values('category').annotate(total=Sum('carbon_footprint'))

        return Response({
            "total_carbon_footprint": total_carbon,
            "breakdown": by_category
        })


#إعداد تقرير PDF

class EmissionReportDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_emissions = EmissionEntry.objects.filter(user=request.user)
        
        # 1. إجمالي البصمة الكربونية
        total_carbon = user_emissions.aggregate(Sum('carbon_footprint'))['carbon_footprint__sum'] or 0
        
        # 2. البيانات التفصيلية (كل العمليات)
        serializer = EmissionSerializer(user_emissions, many=True)
        
        # 3. توزيع الانبعاثات حسب الفئة (مفيد جداً للرسوم البيانية في الـ PDF)
        breakdown = user_emissions.values('category').annotate(total=Sum('carbon_footprint'))

        return Response({
            "report_info": {
                "user": request.user.username,
                "generation_date": timezone.now().strftime("%Y-%m-%d"), # التاريخ الحالي
                "total_carbon_kg": total_carbon,
            },
            "analytics": breakdown,
            "details": serializer.data
        })
