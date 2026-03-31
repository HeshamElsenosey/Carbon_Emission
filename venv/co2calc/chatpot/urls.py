from django.urls import path
from .views import ChatBotView  # تأكد أن اسم الكلاس في views.py هو ChatBotView

urlpatterns = [
    # هذا الرابط سيكون: /api/chatbot/ask/
    path('ask/', ChatBotView.as_view(), name='ask_bot'),
]