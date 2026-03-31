# 🌍 Carbon Emission Tracker (Backend)
> نظام متكامل لحساب وتتبع الانبعاثات الكربونية للأفراد والمؤسسات، مبني باستخدام Django و PostgreSQL.

---

## 🚀 نظرة عامة (Overview)
هذا المشروع هو الجزء الخلفي (Backend) لتطبيق ويب يهدف إلى زيادة الوعي البيئي من خلال حساب البصمة الكربونية بناءً على استهلاك الطاقة، المواصلات، والأنشطة اليومية. يوفر التطبيق نظاماً تجريبياً (Free Trial) ونظام اشتراكات مدفوعة.

## 🛠 التقنيات المستخدمة (Tech Stack)
* **Framework:** Django & Django REST Framework (DRF)
* **Database:** PostgreSQL
* **Security:** Python-Dotenv (Environment Variables)
* **Signals:** Django Signals (Automatic Profile Creation)
* **Version Control:** Git & GitHub

## ✨ المميزات الرئيسية (Features)
- **Authentication:** نظام تسجيل دخول وتوثيق آمن.
- **Auto-Profile:** إنشاء ملف شخصي تلقائياً فور تسجيل المستخدم.
- **Monetization Logic:** نظام فترة تجريبية (14 يوم) مع حماية الـ APIs للمشتركين فقط.
- **Secure Architecture:** فصل البيانات الحساسة تماماً عن الكود البرمجي.
- **Calculation Engine:** خوارزميات دقيقة لحساب معدلات الكربون.

## ⚙️ كيفية التشغيل (Installation & Setup)

1. **تحميل المشروع:**
   ```bash
   git clone [https://github.com/HeshamElsenosey/Carbon_Emission.git](https://github.com/HeshamElsenosey/Carbon_Emission.git)
   cd Carbon_Emission


## 2. Create the virtual environment:

1. **إنشاء البيئة الافتراضية:**
   ```bash
   python -m venv venv
تفعيل البيئة الإفتراضية :
source venv/Scripts/activate