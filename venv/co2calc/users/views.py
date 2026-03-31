from django.shortcuts import render
# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import RegisterSerializer
#****************************************************************************#
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer

class RegisterView(generics.CreateAPIView):
    #todo     نحدد أن هذا الـ View يتعامل مع جدول المستخدمين
    queryset = User.objects.all()
    
    #todo    نستخدم المترجم الذي أنشأناه تواً
    serializer_class = RegisterSerializer
    
    #todo    السماح لأي شخص (زائر) بالوصول لهذا الرابط لإنشاء حساب
    permission_classes = [AllowAny]


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] # ضروري جداً لرفع الملفات

    def post(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    # لسه هنعدل#
    #test update#