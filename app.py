import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# قاموس الكلمات المفتاحية لتسهيل التعديل مستقبلاً
KEYWORDS = {
    "FINANCIAL": ['سعر', 'بكم', 'قيمة', 'ريال', 'تكلفة', 'فاتورة'],
    "TECHNICAL": ['مشكلة', 'عطل', 'بطيء', 'تعليق', 'ما يفتح'],
    "ORDER": ['طلب', 'اشتري', 'توصيل', 'شحن', 'متى يوصل']
}

@app.route('/analyze-task', methods=['POST'])
def smart_analyzer():
    """
    الهدف: تحليل رسائل العملاء القادمة من Make.com وتصنيفها آلياً.
    """
    try:
        # 1. استلام البيانات والتأكد من صحتها
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        message = data.get('text', '').strip()
        sender = data.get('sender', 'عميل غير معروف')

        # 2. منطق التصنيف الذكي (Smart Categorization)
        category = "طلب عام"
        action = "تحويل للمبيعات"

        # تحويل النص للصغير (في حال وجود كلمات إنجليزية)
        msg_lower = message.lower()

        if any(word in msg_lower for word in KEYWORDS["FINANCIAL"]):
            category = "استفسار مالي"
            action = "إرسال قائمة أسعار المنتجات"
        
        elif any(word in msg_lower for word in KEYWORDS["TECHNICAL"]):
            category = "دعم فني"
            action = "فتح تذكرة صيانة فورية"
            
        elif any(word in msg_lower for word in KEYWORDS["ORDER"]):
            category = "طلب شراء"
            action = "تجهيز الشحنة والتواصل مع العميل"

        # 3. بناء الاستجابة الاحترافية
        response_data = {
            "status": "success",
            "analysis": {
                "customer": sender,
                "message_preview": message[:50] + "..." if len(message) > 50 else message,
                "category": category,
                "action": action
            },
            "meta": {
                "engine": "Al-Marwani Smart Analyzer v1.0",
                "processed_at": "توقيت الخادم الحالي"
            }
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    return "Al-Marwani AI Engine is Running Successfully!", 200

if __name__ == '__main__':
    # استخدام المتغيرات البيئية للمنافذ لضمان العمل على Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
