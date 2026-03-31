import os
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv

# 1. تحميل الإعدادات من .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

class ChatBotView(APIView):
    permission_classes = [] 

    def post(self, request):
        user_text = request.data.get('question') or request.data.get('message')
        
        if not user_text:
            return Response({"reply": "فين سؤالك يا بطل؟ 🇪🇬"}, status=status.HTTP_400_BAD_REQUEST)

        # تعليمات الشخصية المصرية
        bot_instructions = (
            "أنت مساعد بيئي مصري 'ابن بلد' وذكي. "
            "تخصصك الوحيد هو البيئة، إعادة التدوير، الاستدامة، وتوفير الطاقة. "
            "تعليمات صارمة: ممنوع تماماً الإجابة على أي سؤال خارج مجال البيئة (مثل الرياضة، السياسة، الفن، أو أسئلة عامة). "
            "لو المستخدم سألك في موضوع خارج البيئة، اعتذر بلباقة بالعامية وقوله إن ده مش تخصصك ووجهه لموضوع بيئي. "
            "جاوب بالعامية المصرية المختصرة جداً. ادخل في الإجابة علطول بدون مقدمات واستخدم إيموجي مناسب."
        )

        try:
            # 2. البحث التلقائي عن الموديل المتاح في حسابك (لتجنب خطأ 404)
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # محاولة اختيار gemini-pro كخيار أول لأنه الأكثر استقراراً في منطقتنا
            selected_model = ""
            if "models/gemini-pro" in model_list:
                selected_model = "gemini-pro"
            elif "models/gemini-1.5-flash" in model_list:
                selected_model = "gemini-1.5-flash"
            else:
                selected_model = model_list[0].replace("models/", "")

            print(f"✅ الموديل المستخدم حالياً: {selected_model}") # سيظهر لك في Terminal

            model = genai.GenerativeModel(selected_model)
            
            # 3. توليد الرد
            full_prompt = f"{bot_instructions}\nسؤال المستخدم: {user_text}"
            response = model.generate_content(full_prompt)

            return Response({
                "reply": response.text,
                "status": "success",
                "model_used": selected_model
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ Chatbot Error: {str(e)}")
            return Response({
                "reply": f"حصل خطأ فني: {str(e)}",
                "status": "error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
